#!/usr/bin/env python3
"""Prepare SKU discount changes from an exported snapshot. No online submission."""
import argparse
import json
import math
from pathlib import Path

def percent(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 100:
        raise ValueError('Discount percent must be finite and between 0 and 100')
    return value

def plan(data):
    if any(not data.get(k) for k in ('store_ref', 'marketplace', 'snapshot_at', 'evidence_id')):
        raise ValueError('Explicit store, marketplace, timestamp and evidence are required')
    targets = data.get('targets', [])
    if not targets:
        raise ValueError('No target SKU supplied')
    seen, output = set(), []
    for target in targets:
        sku = target.get('sku')
        if not isinstance(sku, str) or not sku.strip():
            raise ValueError('SKU must be nonempty')
        key = (sku, target.get('promotion_id'))
        if key in seen:
            raise ValueError('Duplicate target SKU and activity')
        seen.add(key)
        desired = percent(target.get('target_percent'))
        matches = [(a, item) for a in data.get('activities', []) for item in a.get('items', [])
                   if item.get('sku') == sku and (not target.get('promotion_id') or a.get('promotion_id') == target['promotion_id'])]
        row = {'sku': sku, 'target_percent': desired, 'status': 'HOLD'}
        if len(matches) != 1:
            row['reason'] = 'SKU activity is missing or ambiguous'
        else:
            activity, item = matches[0]
            current = item.get('discount_percent')
            row.update({'promotion_id': activity.get('promotion_id'), 'before_percent': current,
                        'activity_status': activity.get('status')})
            if not row['promotion_id'] or current is None or not activity.get('status'):
                row['reason'] = 'Incomplete activity or previous discount'
            else:
                current = percent(current)
                if activity.get('status', '').upper() in {'RUNNING', 'ACTIVE'} and desired < current:
                    row['reason'] = 'Reducing a running discount requires current platform rule verification'
                else:
                    row.update(status='NO_CHANGE' if desired == current else 'DRAFT', reason='Recheck snapshot before any authorized submission')
        output.append(row)
    return {'status': 'HOLD' if any(x['status'] == 'HOLD' for x in output) else 'DRAFT',
            'mode': 'OFFLINE_PLAN', 'store_ref': data['store_ref'], 'marketplace': data['marketplace'],
            'snapshot_at': data['snapshot_at'], 'evidence_id': data['evidence_id'], 'changes': output,
            'submitted': False}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = plan(json.loads(args.input.read_text(encoding='utf-8')))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8') as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write('\n')
    print(json.dumps({'status': result['status'], 'submitted': False}))

if __name__ == '__main__':
    main()
