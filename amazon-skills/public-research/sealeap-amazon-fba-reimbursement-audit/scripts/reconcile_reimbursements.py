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

def run(data):
    scope = obj(data.get("scope"), "scope")
    for key in ("store_id", "marketplace", "currency", "as_of"):
        text(scope.get(key), f"scope.{key}")
    date.fromisoformat(scope["as_of"])
    records = data.get("records")
    if not isinstance(records, list) or not records:
        raise ValueError("records: expected a non-empty list")
    seen, output = set(), []
    review_total = Decimal(0)
    for raw in records:
        row = obj(raw, "record")
        event = text(row.get("event_id"), "event_id")
        if event in seen:
            raise ValueError("duplicate loss event_id; reconcile payments before input")
        seen.add(event)
        sku = text(row.get("sku"), "sku")
        if row.get("currency") != scope["currency"]:
            raise ValueError(f"{event}: currency mismatch")
        result = {"event_id": event, "sku": sku, "status": "HOLD",
                  "basis_total": None, "additional_review_candidate": None,
                  "reasons": []}
        if row.get("event_stage") != "before_customer_order":
            result["reasons"].append("STAGE_REQUIRES_MANUAL_POLICY_REVIEW")
            output.append(result)
            continue
        for key in ("documented_unit_cost", "already_reimbursed_net", "policy_unit_cap",
                    "affected_units"):
            if row.get(key) is None:
                result["reasons"].append("MISSING_" + key.upper())
        for key in ("policy_eligibility_verified", "unit_basis_verified"):
            if row.get(key) is not True:
                result["reasons"].append(key.upper())
        if row.get("reimbursement_window_status") != "open":
            result["reasons"].append("REVIEW_WINDOW_NOT_CONFIRMED_OPEN")
        evidence = row.get("evidence_ids")
        if not isinstance(evidence, list) or not evidence or not all(
                isinstance(x, str) and x.strip() for x in evidence):
            result["reasons"].append("COST_EVIDENCE_MISSING")
        if result["reasons"]:
            output.append(result)
            continue
        units = integer(row["affected_units"], "affected_units", 1)
        cost = number(row["documented_unit_cost"], "documented_unit_cost")
        paid = number(row["already_reimbursed_net"], "already_reimbursed_net")
        cap = number(row["policy_unit_cap"], "policy_unit_cap")
        if cap == 0:
            raise ValueError("policy_unit_cap must be positive")
        if cost == 0:
            result["reasons"].append("ZERO_COST_REQUIRES_MANUAL_REVIEW")
            output.append(result)
            continue
        basis = min(cost, cap) * units
        gap = basis - paid
        candidate = max(Decimal(0), gap)
        result.update(status="PASS", basis_total=basis,
                      already_reimbursed_net=paid, signed_gap=gap,
                      additional_review_candidate=candidate,
                      evidence_ids=evidence,
                      reasons=["PAID_EXCEEDS_BASIS_REVIEW"] if gap < 0 else [])
        review_total += candidate
        output.append(result)
    excluded = sum(row["status"] == "HOLD" for row in output)
    return {"status": "HOLD" if excluded else "PASS", "scope": scope,
            "amount_kind": "ESTIMATE_FOR_REVIEW_NOT_RECEIVABLE",
            "review_candidate_total_for_pass_rows": review_total,
            "excluded_records": excluded, "records": output,
            "submission_performed": False}


if __name__ == "__main__":
    sys.exit(main())
