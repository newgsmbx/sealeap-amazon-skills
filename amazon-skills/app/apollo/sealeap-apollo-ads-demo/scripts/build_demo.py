#!/usr/bin/env python3
"""Write a standalone synthetic Amazon Ads rule demo; no network or installation."""
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1] / 'assets' / 'demo.html'
    page = source.read_text(encoding='utf-8')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8') as handle:
        handle.write(page)
    print(str(args.output.resolve()))

if __name__ == '__main__':
    main()
