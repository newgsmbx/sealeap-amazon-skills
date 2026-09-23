#!/usr/bin/env python3
"""Offline calculation only; never calls an account API or submits changes."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation, ROUND_CEILING
from pathlib import Path


def text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label}: expected non-empty text")
    return value.strip()


def number(value, label):
    if isinstance(value, bool):
        raise ValueError(f"{label}: boolean is not a number")
    try:
        result = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f"{label}: expected a finite non-negative number") from exc
    if not result.is_finite() or result < 0 or result > Decimal("1e15"):
        raise ValueError(f"{label}: expected a finite number in [0, 1e15]")
    return result


def integer(value, label, minimum=0):
    if type(value) is not int or value < minimum or value > 1000000000000000:
        raise ValueError(f"{label}: expected integer >= {minimum}")
    return value


def obj(value, label):
    if not isinstance(value, dict):
        raise ValueError(f"{label}: expected object")
    return value


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f"non-finite JSON constant: {value}")


def ratio(numerator, denominator):
    if numerator is None or denominator is None or denominator == 0:
        return None
    return (Decimal(numerator) / Decimal(denominator)).quantize(Decimal("0.000001"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"),
                          object_pairs_hook=unique_keys,
                          parse_float=Decimal, parse_constant=reject_constant)
        result = run(obj(data, "input"))
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str, allow_nan=False))
        return 2 if result["status"] == "HOLD" else 0
    except (ValueError, TypeError, OSError, InvalidOperation) as exc:
        print(json.dumps({"status": "INVALID", "error": str(exc)}, ensure_ascii=False))
        return 1

STAGES = ("impressions", "clicks", "cart_adds", "purchases")
FIELDS = ("query_volume",) + tuple(f"{owner}_{stage}" for stage in STAGES
                                  for owner in ("market", "entity"))
SCOPE_KEYS = ("account_id", "marketplace", "view", "entity_id",
              "report_definition", "timezone")


def scope_match(row, scope):
    for key in SCOPE_KEYS:
        if key in row and row[key] != scope[key]:
            raise ValueError(f"mixed scope: {key}")


def run(data):
    scope = obj(data.get("scope"), "scope")
    for key in SCOPE_KEYS:
        text(scope.get(key), f"scope.{key}")
    if scope["view"] not in ("BRAND", "ASIN"):
        raise ValueError("view must be BRAND or ASIN")
    start = date.fromisoformat(text(data.get("window_start"), "window_start"))
    end = date.fromisoformat(text(data.get("window_end"), "window_end"))
    if end < start:
        raise ValueError("analysis window is reversed")
    periods = data.get("periods")
    if not isinstance(periods, list) or not periods:
        raise ValueError("periods: expected non-empty list")
    ids, windows, issues = set(), [], []
    for raw in periods:
        period = obj(raw, "period")
        pid = text(period.get("id"), "period.id")
        if pid in ids:
            raise ValueError("duplicate period id")
        ids.add(pid)
        scope_match(period, scope)
        a = date.fromisoformat(text(period.get("start"), "period.start"))
        b = date.fromisoformat(text(period.get("end"), "period.end"))
        if b < a or a < start or b > end:
            raise ValueError("period reversed or outside window; no proportional slicing")
        windows.append((a, b, pid))
        if period.get("complete") is not True:
            issues.append(f"PERIOD_NOT_COMPLETE:{pid}")
        if period.get("mature") is not True:
            issues.append(f"PERIOD_NOT_MATURE:{pid}")
    windows.sort()
    previous = start - timedelta(days=1)
    for a, b, pid in windows:
        if a <= previous:
            raise ValueError("overlapping periods; cannot combine quarterly/monthly overlap")
        if a != previous + timedelta(days=1):
            issues.append(f"PERIOD_COVERAGE_GAP_BEFORE:{pid}")
        previous = b
    if previous != end:
        issues.append("PERIOD_COVERAGE_GAP_AT_END")
    rows = data.get("rows")
    if not isinstance(rows, list):
        raise ValueError("rows: expected list")
    queries, seen = {}, set()
    for raw in rows:
        row = obj(raw, "row")
        pid = text(row.get("period_id"), "row.period_id")
        if pid not in ids:
            raise ValueError("row refers to unknown period")
        query = text(row.get("query"), "query")
        key = (pid, query)
        if key in seen:
            raise ValueError("duplicate query-period row")
        seen.add(key)
        scope_match(row, scope)
        counts = {field: None if row.get(field) is None else integer(row[field], field)
                  for field in FIELDS}
        for stage in STAGES:
            entity, market = counts["entity_" + stage], counts["market_" + stage]
            if entity is not None and market is not None and entity > market:
                raise ValueError(f"entity {stage} exceeds market count")
        queries.setdefault(query, {})[pid] = counts
    if not rows:
        issues.append("NO_QUERY_ROWS")
    result = []
    for query, per_period in sorted(queries.items()):
        observed, totals, coverage = {}, {}, {}
        missing_periods = sorted(ids - per_period.keys())
        for field in FIELDS:
            values = [counts[field] for counts in per_period.values()
                      if counts[field] is not None]
            coverage[field] = len(values)
            observed[field] = sum(values) if values else None
            totals[field] = (observed[field] if not issues and len(values) == len(ids)
                             else None)
        partial = any(value is None for value in totals.values())
        metrics = {stage + "_share": ratio(totals["entity_" + stage],
                                           totals["market_" + stage])
                   for stage in STAGES}
        metrics["entity_clicks_per_impression"] = ratio(
            totals["entity_clicks"], totals["entity_impressions"])
        metrics["entity_purchases_per_click"] = ratio(
            totals["entity_purchases"], totals["entity_clicks"])
        result.append({"query": query, "status": "HOLD" if partial else "PASS",
                       "missing_periods": missing_periods,
                       "metric_period_coverage": coverage,
                       "observed_partial_counts": observed, "full_window_counts": totals,
                       "metrics_fraction": metrics})
    return {"status": "HOLD" if issues or any(r["status"] == "HOLD" for r in result)
            else "PASS", "scope": scope, "window_start": start.isoformat(),
            "window_end": end.isoformat(), "period_count": len(ids),
            "coverage_issues": issues, "queries": result,
            "business_order_reconciliation": "NOT_ASSERTED"}


if __name__ == "__main__":
    sys.exit(main())
