#!/usr/bin/env python3
"""Calculate unit advertising economics from explicit, evidenced inputs; offline."""
import argparse
import json
import math
from pathlib import Path

COSTS = ('purchase', 'inbound', 'platform', 'fulfillment', 'storage', 'returns', 'other')
LABELS = {'FACT', 'ESTIMATE', 'ASSUMPTION', 'UNKNOWN'}

def unique(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError('duplicate JSON key: ' + key)
        out[key] = value
    return out

def calculate(data):
    currency = data.get('currency')
    if not isinstance(currency, str) or len(currency) != 3 or not currency.isupper():
        raise ValueError('currency must be an explicit three-letter code')
    gaps = []
    evidence = {e['id']: e for e in data.get('evidence', [])}
    if len(evidence) != len(data.get('evidence', [])):
        raise ValueError('duplicate evidence ID')

    def number(cell, key, money=False, ratio=False):
        if cell is None or not isinstance(cell, dict) or cell.get('value') is None:
            gaps.append(key + ': missing value')
            return None
        value = cell['value']
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
            raise ValueError(key + ': value must be finite and nonnegative')
        if money and cell.get('currency') != currency:
            raise ValueError(key + ': currency mismatch or missing currency')
        if ratio and value > 1:
            raise ValueError(key + ': use a ratio from 0 to 1')
        label = cell.get('label')
        if label not in LABELS:
            raise ValueError(key + ': invalid evidence label')
        if label == 'UNKNOWN':
            gaps.append(key + ': evidence is UNKNOWN')
        record = evidence.get(cell.get('evidence_id'), {})
        if any(not record.get(k) for k in ('source', 'collected_at', 'data_period')):
            gaps.append(key + ': incomplete evidence')
        return value

    price = number(data.get('net_revenue_per_unit'), 'net_revenue_per_unit', money=True)
    ad_revenue = number(data.get('ad_revenue_per_order'), 'ad_revenue_per_order', money=True)
    costs = [number(data.get('unit_costs', {}).get(k), 'unit_costs.' + k, money=True) for k in COSTS]
    acos = number(data.get('target_acos'), 'target_acos', ratio=True)
    cvr = number(data.get('ad_cvr'), 'ad_cvr', ratio=True)
    if price == 0 or ad_revenue == 0:
        raise ValueError('revenue denominators must be positive')
    contribution = None if price is None or any(x is None for x in costs) else price - sum(costs)
    cpa = None if ad_revenue is None or acos is None else ad_revenue * acos
    return {
        'status': 'HOLD' if gaps else 'CALCULATED', 'currency': currency, 'gaps': gaps,
        'contribution_before_ads': contribution,
        'break_even_acos': None if contribution is None or ad_revenue is None else contribution / ad_revenue,
        'target_cpa': cpa, 'max_cpc': None if cpa is None or cvr is None else cpa * cvr,
        'contribution_at_target_acos': None if contribution is None or cpa is None else contribution - cpa,
        'note': 'Calculation only; inputs retain their evidence labels. Not an approval to launch ads.',
        'input': data,
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding='utf-8'), object_pairs_hook=unique)
    result = calculate(data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8') as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write('\n')
    print(json.dumps({'status': result['status'], 'output': str(args.output.resolve())}))

if __name__ == '__main__':
    main()
