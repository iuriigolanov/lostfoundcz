#!/usr/bin/env python3
"""Sync /menu/ (EN) from the home-page menu accordion (index.html).

The home page is the source of truth. Run after build-menu.py or any manual
menu edit:  python tools/sync-menu-page.py
Regenerates in menu/index.html: every category list (names, 💪 strength,
allergens, prices, ingredients, notes), the strength legend, the jump links
and the Menu JSON-LD. Halloween/seasonal categories keep their hw-only class.
"""
import re, json, html, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'index.html')
DST = os.path.join(ROOT, 'menu', 'index.html')

# home-page category id -> (menu-page anchor, intro paragraph)
CATS = {
 'cat-halloween': ('halloween-specials', 'Limited-time Halloween cocktails &amp; shots — available all November.'),
 'cat-signature': ('signature-cocktails', "Exclusive creations by our bartenders — you won't find these anywhere else in Prague."),
 'cat-classic':   ('classic-cocktails', 'All the classics: Espresso Martini, Negroni, Mojito, Mai Tai, Margarita, Old Fashioned and more.'),
 'cat-wine':      ('wine-cocktails-spritz', 'Spritzes, Mimosa and wine-based cocktails.'),
 'cat-shots':     ('special-shots', 'Signature shots and shot sets for the whole table.'),
 'cat-hookah':    ('hookah', 'Premium hookah, one price for every blend. <a href="/hookah/">More about our hookah lounge →</a>'),
 'cat-nonalco':   ('non-alcoholic', 'Alcohol-free 0.0% cocktails and homemade lemonades.'),
 'cat-food':      ('food', 'Stone-baked pizza and quesadillas from our kitchen, plus nachos, nuts and chips.'),
}

def txt(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s)).strip()

def parse():
    s = open(SRC, encoding='utf-8').read()
    cats = []
    for m in re.finditer(r'<details class="menu-cat([^"]*)"[^>]*id="([^"]+)">\s*<summary[^>]*>(.*?)</summary>(.*?)</details>', s, re.S):
        extra, cid, summ, body = m.groups()
        if cid not in CATS:
            continue
        title = txt(re.search(r'<span class="cat-title">(.*?)</span>', summ).group(1))
        flat = re.search(r'<span class="cat-flat">([^<]*)</span>', summ)
        flat = re.sub(r'\D', '', flat.group(1)) if flat else None
        items = []
        for it in re.findall(r'<div class="mi">(.*?)\n      </div>', body, re.S):
            head = re.search(r'<div class="mi-head">(.*?)</div>', it, re.S).group(1)
            name = re.search(r'<span class="mi-name">(.*?)</span>', head).group(1)
            al = re.search(r'data-tip="([^"]*)">\(([^)]*)\)', head)
            sc = re.search(r'(<span class="lf-str[^"]*" title="[^"]*">.*?</span>)', head)
            pr = re.search(r'<span class="mi-price">([^<]*)</span>', head)
            desc = re.search(r'<div class="mi-desc">(.*?)</div>', it, re.S).group(1)
            note = re.search(r'<div class="mi-note">(.*?)</div>', it, re.S)
            items.append(dict(name=name, allerg=al.group(2) if al else None, tip=al.group(1) if al else None,
                              scale=sc.group(1) if sc else '', price=(pr.group(1) if pr else flat),
                              desc=desc, note=note.group(1) if note else None))
        cats.append(dict(id=cid, title=title, seasonal='hw-only' in extra, items=items))
    legend = re.search(r'(<div class="lf-legend">.*?</div>)', s, re.S).group(1)
    return cats, legend

def build(cats, legend):
    out = []
    for c in cats:
        anchor, intro = CATS[c['id']]
        cls = ' class="hw-only"' if c['seasonal'] else ''
        wrap_o = f'<div class="hw-only">\n' if c['seasonal'] else ''
        wrap_c = '</div>\n' if c['seasonal'] else ''
        lis = []
        for i in c['items']:
            al = f' <em class="al" title="Allergens: {i["tip"]}">({i["allerg"]})</em>' if i['allerg'] else ''
            pr = f' <span>{i["price"]} Kč</span>' if i['price'] else ''
            note = f'<small class="note">{i["note"]}</small>' if i['note'] else ''
            lis.append(f'    <li><b>{i["name"]}{al}{i["scale"]}{pr}</b><small>{i["desc"]}</small>{note}</li>')
        out.append(f'{wrap_o}  <h2 id="{anchor}">{html.escape(c["title"], quote=False)}</h2>\n  <p>{intro}</p>\n  <ul class="items">\n' + '\n'.join(lis) + f'\n  </ul>\n{wrap_c}')
    return legend, ''.join(out)

def jsonld(cats):
    secs = []
    for c in cats:
        if c['seasonal']:
            continue
        its = []
        for i in c['items']:
            d = {"@type": "MenuItem", "name": txt(i['name']), "description": txt(i['desc'])}
            if i['price']:
                d["offers"] = {"@type": "Offer", "price": txt(i['price']), "priceCurrency": "CZK"}
            its.append(d)
        secs.append({"@type": "MenuSection", "name": re.sub(r'^[^A-Za-z0-9]+', '', c['title']), "hasMenuItem": its})
    return json.dumps({"@context": "https://schema.org", "@type": "Menu", "name": "Lost & Found Bar Prague — Full Menu",
                       "inLanguage": "en", "hasMenuSection": secs, "url": "https://lostfoundcz.com/menu/"}, ensure_ascii=False)

def main():
    cats, legend = parse()
    legend, body = build(cats, legend)
    p = open(DST, encoding='utf-8').read()
    start = p.index('<h2 id=', p.index('<ul class="facts">'))
    end = p.index('<p style="margin-top:22px">')
    p = p[:start] + legend + '\n' + body + '  ' + p[end:]
    p = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "Menu".*?</script>',
               lambda m: '<script type="application/ld+json">' + jsonld(cats) + '</script>', p, count=1, flags=re.S)
    # jump links
    tl = ''.join(f'<li class="tl{" hw-only" if c["seasonal"] else ""}"><a href="#{CATS[c["id"]][0]}">{html.escape(c["title"], quote=False)}</a></li>' for c in cats)
    p = re.sub(r'(<li class="tl[^"]*">.*?</li>)+', tl, p, count=1, flags=re.S)
    open(DST, 'w', encoding='utf-8').write(p)
    print('menu/index.html synced:', sum(len(c['items']) for c in cats), 'items in', len(cats), 'categories')

if __name__ == '__main__':
    main()
