#!/usr/bin/env python3
"""Check a title CSV against an explicitly supplied marketplace policy; offline."""
import argparse
import csv
import json
import re
from pathlib import Path

REQUIRED = {'sku', 'marketplace', 'product_type', 'title', 'highlight'}

def check(row, policy):
    method = policy.get('count_method', 'codepoints')
    if method not in {'codepoints', 'utf16'}:
        raise ValueError('count_method must be codepoints or utf16')
    count = (lambda s: len(s)) if method == 'codepoints' else (lambda s: len(s.encode('utf-16-le')) // 2)
    title, highlight = row.get('title', ''), row.get('highlight', '')
    result = {'title_characters': count(title), 'highlight_characters': count(highlight)}
    if policy.get('verified') is not True or not all(policy.get(k) for k in ('source', 'checked_at', 'marketplace', 'product_types')):
        return {**result, 'check_status': 'HOLD', 'issues': 'Policy scope or evidence not verified'}
    if row.get('marketplace') != policy['marketplace'] or row.get('product_type') not in policy['product_types']:
        return {**result, 'check_status': 'HOLD', 'issues': 'Row is outside the verified policy scope'}
    errors = []
    if not title.strip():
        errors.append('Title is empty')
    if policy.get('highlight_required') and not highlight.strip():
        errors.append('Highlight is required')
    for field, value in [('title', title), ('highlight', highlight)]:
        maximum = policy.get(field + '_max')
        if isinstance(maximum, bool) or not isinstance(maximum, int) or maximum <= 0:
            raise ValueError(field + '_max must be an explicit positive integer')
        if count(value) > maximum:
            errors.append(field + ' exceeds ' + str(maximum))
        for char in policy.get('banned_characters', []):
            if char in value:
                errors.append(field + ' contains a prohibited character')
        for term in policy.get('banned_phrases', []):
            if term.casefold() in value.casefold():
                errors.append(field + ' contains a prohibited phrase')
        repeat = policy.get('max_word_repeat')
        if repeat is not None:
            if isinstance(repeat, bool) or not isinstance(repeat, int) or repeat < 1:
                raise ValueError('max_word_repeat must be a positive integer')
            words = re.findall(r"[^\W_]+", value.casefold(), flags=re.UNICODE)
            exempt = {x.casefold() for x in policy.get('repeat_exempt_words', [])}
            if any(words.count(w) > repeat for w in set(words) - exempt):
                errors.append(field + ' exceeds the specified word repetition rule')
    return {**result, 'check_status': 'FAIL' if errors else 'PASS', 'issues': '; '.join(sorted(set(errors)))}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--policy', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    policy = json.loads(args.policy.read_text(encoding='utf-8'))
    with args.input.open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        if not REQUIRED <= set(reader.fieldnames or []):
            raise ValueError('Required columns: ' + ', '.join(sorted(REQUIRED)))
        fields = reader.fieldnames
        rows = list(reader)
    if not rows:
        raise ValueError('Input has no data rows')
    results = [{**r, **check(r, policy)} for r in rows]
    added = ['title_characters', 'highlight_characters', 'check_status', 'issues']
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=[k for k in fields if k not in added] + added)
        writer.writeheader()
        writer.writerows(results)
    print(json.dumps({s: sum(r['check_status'] == s for r in results) for s in ('PASS', 'FAIL', 'HOLD')}))

if __name__ == '__main__':
    main()
