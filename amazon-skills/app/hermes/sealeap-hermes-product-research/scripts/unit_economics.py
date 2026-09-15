#!/usr/bin/env python3
"""Calculate per-sellable-unit contribution from explicitly scoped evidence.

No network, provider calls, or file writes. Exit 0: calculated; 2: incomplete
evidence; 1: invalid input. Currency amounts use Decimal and output as strings.
"""
import argparse
from datetime import datetime
from decimal import Decimal, InvalidOperation, localcontext
import json
from pathlib import Path
import re
import sys

COST_KEYS = ('procurement', 'inbound', 'fulfillment', 'storage', 'platform_fees',
             'duties_and_nonrecoverable_tax', 'expected_return_loss', 'other_variable')
EVIDENCE_TYPES = {'FACT', 'ESTIMATE', 'ASSUMPTION', 'UNKNOWN'}
SCOPE_KEYS = ('platform', 'marketplace', 'product_id', 'currency', 'period',
              'sellable_unit', 'unit_evidence', 'revenue_basis')


class InvalidInput(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise InvalidInput(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result


def nonblank(value):
    return isinstance(value, str) and bool(value.strip())


def evidence_value(obj, label, currency, missing, types):
    if obj is None:
        missing.append({'field': label, 'reason': 'not supplied'})
        return None
    require(isinstance(obj, dict), label + ': expected an evidence object')
    unknown_keys = set(obj) - {'value', 'currency', 'evidence_type', 'source', 'observed_at', 'missing_reason'}
    require(not unknown_keys, label + ': unsupported evidence fields')
    kind = obj.get('evidence_type')
    require(kind in EVIDENCE_TYPES, label + ': invalid or missing evidence_type')
    if obj.get('value') is None or kind == 'UNKNOWN':
        require(obj.get('value') is None, label + ': UNKNOWN evidence must not contain a numeric value')
        require(nonblank(obj.get('missing_reason')), label + ': missing_reason is required')
        missing.append({'field': label, 'reason': obj['missing_reason']})
        return None
    require(obj.get('currency') == currency, label + ': currency differs from scope')
    require(nonblank(obj.get('source')), label + ': source is required, including for zero')
    require(nonblank(obj.get('observed_at')), label + ': observed_at is required')
    try:
        timestamp = datetime.fromisoformat(obj['observed_at'].replace('Z', '+00:00'))
    except ValueError as exc:
        raise InvalidInput(label + ': invalid ISO observed_at') from exc
    require(timestamp.tzinfo is not None, label + ': observed_at must include timezone')
    raw = obj['value']
    require(isinstance(raw, (str, int, float, Decimal)) and not isinstance(raw, bool),
            label + ': value must be a decimal amount')
    try:
        value = Decimal(str(raw))
    except InvalidOperation as exc:
        raise InvalidInput(label + ': invalid decimal') from exc
    require(value.is_finite() and value >= 0, label + ': value must be finite and nonnegative')
    require(value <= Decimal('1000000000000'), label + ': amount exceeds per-unit model range')
    require(value.as_tuple().exponent >= -6, label + ': amount supports at most six decimal places')
    types.add(kind)
    return value


def formatted(value):
    return str(value.quantize(Decimal('0.000001')))


def calculate(data):
    require(isinstance(data, dict), 'Input must be an object')
    require(data.get('schema_version') == 1 and not isinstance(data.get('schema_version'), bool),
            'schema_version must be 1')
    require(not (set(data) - {'schema_version', 'scope', 'revenue', 'costs', 'ad_cost_per_unit',
                              'ad_sales_revenue_basis'}), 'Unsupported top-level fields')
    scope = data.get('scope')
    require(isinstance(scope, dict), 'scope is required')
    require(set(scope) == set(SCOPE_KEYS), 'scope must contain exactly the documented fields')
    require(all(nonblank(scope[k]) for k in SCOPE_KEYS), 'Scope fields must be nonempty strings')
    require(bool(re.fullmatch('[A-Z]{3}', scope['currency'])), 'currency must be a three-letter code')
    costs = data.get('costs', {})
    require(isinstance(costs, dict), 'costs must be an object')
    require(not (set(costs) - set(COST_KEYS)), 'Unsupported cost category; normalize into other_variable')
    missing, types = [], set()
    currency = scope['currency']
    revenue = evidence_value(data.get('revenue'), 'revenue', currency, missing, types)
    values = {key: evidence_value(costs.get(key), 'costs.' + key, currency, missing, types)
              for key in COST_KEYS}
    ad_cost = evidence_value(data.get('ad_cost_per_unit'), 'ad_cost_per_unit', currency, missing, types)
    if revenue is not None:
        require(revenue > 0, 'revenue must be positive for this per-unit model')
    ad_basis = data.get('ad_sales_revenue_basis')
    require(ad_basis is None or nonblank(ad_basis), 'ad_sales_revenue_basis must be a nonempty string or null')
    result = {'status': 'HOLD' if missing else 'CALCULATED', 'scope': scope,
              'calculation_basis': sorted(types), 'missing': missing,
              'metrics': None, 'decision': 'NOT_A_PROCUREMENT_DECISION',
              'limitations': ['Per sellable unit; fixed overhead, financing and cash timing are not calculated.',
                              'Evidence labels and scope are declared by input, not independently verified.']}
    if missing:
        return result
    with localcontext() as ctx:
        ctx.prec = 40
        non_ad = sum(values.values(), Decimal(0))
        before = revenue - non_ad
        after = before - ad_cost
        comparable = ad_basis == scope['revenue_basis']
        if not comparable:
            be, reason = None, 'Ad revenue denominator is missing or differs from revenue_basis'
        elif before < 0:
            be, reason = None, 'Negative contribution before ads; no nonnegative break-even ACOS'
        else:
            be, reason = formatted(before / revenue), None
        result['metrics'] = {
            'currency': currency, 'revenue_per_unit': formatted(revenue),
            'non_ad_variable_cost_per_unit': formatted(non_ad),
            'contribution_before_ads_per_unit': formatted(before),
            'ad_cost_per_unit': formatted(ad_cost),
            'contribution_after_ads_per_unit': formatted(after),
            'contribution_margin_ratio': formatted(after / revenue),
            'blended_ad_cost_share_ratio': formatted(ad_cost / revenue),
            'break_even_acos_ratio': be, 'break_even_acos_missing_reason': reason,
        }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path, help='Scoped per-unit evidence JSON')
    args = parser.parse_args()
    try:
        require(args.input.stat().st_size <= 1024 * 1024, 'Input exceeds 1 MiB')
        data = json.loads(args.input.read_text(encoding='utf-8'),
                          object_pairs_hook=unique_object, parse_float=Decimal,
                          parse_constant=lambda _: (_ for _ in ()).throw(InvalidInput('Non-finite JSON number')))
        result = calculate(data)
    except (OSError, UnicodeError, InvalidInput, json.JSONDecodeError) as exc:
        print(json.dumps({'status': 'INVALID_INPUT', 'error': str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if result['status'] == 'HOLD' else 0


if __name__ == '__main__':
    sys.exit(main())
