#!/usr/bin/env python3
"""Update the Google review count everywhere on the site + bump sitemap lastmod.
Usage (from repo root):  python tools/bump-reviews.py 1385
Handles all three formats: 1,370 (EN) · 1.370 (DE) · 1 370 (CS/UA, incl. nbsp)."""
import re, sys, datetime, pathlib

FILES = ['index.html', 'cs/index.html', 'de/index.html', 'ua/index.html',
         'catering-calculator/index.html', 'hookah/index.html']
PAGES = ['', 'cs/', 'de/', 'ua/', 'catering-calculator/', 'hookah/']

def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit() or len(sys.argv[1]) != 4:
        sys.exit('usage: python tools/bump-reviews.py 1385')
    new = sys.argv[1]
    root = pathlib.Path(__file__).resolve().parent.parent
    # current count = the one in EN grp-count block
    en = (root / 'index.html').read_text(encoding='utf-8')
    m = re.search(r'grp-count">(\d)[,.]?(\d{3})\+', en)
    if not m:
        sys.exit('could not find current count in index.html')
    old = m.group(1) + m.group(2)
    if old == new:
        sys.exit(f'already {new}')
    pat = re.compile(r'(?<!\d)' + old[0] + r'([,.   ]?)' + old[1:] + r'(?!\d)')
    total = 0
    for f in FILES:
        p = root / f
        s = p.read_text(encoding='utf-8')
        s2, n = pat.subn(lambda mm: new[0] + mm.group(1) + new[1:], s)
        if n:
            p.write_text(s2, encoding='utf-8')
        total += n
        print(f'{f:34} {n}')
    sm = root / 'sitemap.xml'
    x = sm.read_text(encoding='utf-8')
    today = datetime.date.today().isoformat()
    for pg in PAGES:
        x = re.sub(r'(<loc>https://lostfoundcz\.com/%s</loc>\s*<lastmod>)[^<]+' % re.escape(pg),
                   r'\g<1>' + today, x, count=1)
    sm.write_text(x, encoding='utf-8')
    print(f'{old} -> {new}: {total} replacements, sitemap lastmod = {today}')

if __name__ == '__main__':
    main()
