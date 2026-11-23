#!/usr/bin/env python3
"""Sync the standalone menu pages from the home-page menu accordion.

  index.html     -> menu/index.html     (EN)
  cs/index.html  -> cs/menu/index.html  (CS)

The home page of each language is the source of truth (it is itself built
from tools/menu-data.json by build-menu.py, which calls this script at the end).
Run manually:  python tools/sync-menu-page.py

Regenerated in each menu page (between <!-- menu:...:start/end --> markers):
  * top block: one-line key facts, "Find your drink" / "Menu photos" buttons,
    sticky category bar
  * every category list (names, 💪 strength, allergens, prices, ingredients, notes);
    seasonal categories (hw-only) keep their auto-hide class
  * FAQ + FAQPage JSON-LD (prices/counts computed from the menu)
  * Menu JSON-LD, lead/meta counts ("60 cocktails from 165 Kč")
Idempotent: running it twice gives the same file.
"""
import re, json, html, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# featured signature cocktails named in the FAQ (edit order here)
FEATURED = ['Ferrari', 'Lamborghini', 'Skittles', 'Killer', 'Wolf Blood', 'Crimson Kiss', 'Panagel Tonic']

ANCHORS = {'cat-halloween': 'halloween-specials', 'cat-signature': 'signature-cocktails', 'cat-classic': 'classic-cocktails',
           'cat-wine': 'wine-cocktails-spritz', 'cat-shots': 'special-shots', 'cat-hookah': 'hookah',
           'cat-nonalco': 'non-alcoholic', 'cat-food': 'food'}

LANGS = {
 'en': dict(
  src='index.html', dst='menu/index.html', home='/', url='https://lostfoundcz.com/menu/', inlang='en',
  intro={
   'cat-halloween': 'Limited-time Halloween cocktails &amp; shots — available all November.',
   'cat-signature': "Exclusive creations by our bartenders — you won't find these anywhere else in Prague.",
   'cat-classic': 'All the classics: Espresso Martini, Negroni, Mojito, Mai Tai, Margarita, Old Fashioned and more.',
   'cat-wine': 'Spritzes, Mimosa and wine-based cocktails.',
   'cat-shots': 'Signature shots and shot sets for the whole table.',
   'cat-hookah': 'Premium hookah, one price for every blend. <a href="/hookah/">More about our hookah lounge →</a>',
   'cat-nonalco': 'Alcohol-free 0.0% cocktails and homemade lemonades.',
   'cat-food': 'Stone-baked pizza and quesadillas from our kitchen, plus nachos, nuts and chips.'},
  facts=lambda v: f'🍸 Signature cocktails from {v["s_lo"]} Kč · 🌿 Hookah {v["hook"]} Kč · 🍕 Pizza &amp; quesadillas · 0.0% alcohol-free cocktails · 💳 Card &amp; cash',
  finder='🍹 Find your drink', photos='📸 View full menu (photos)', nav_label='Menu categories',
  count_re=(r'\d+ cocktails from \d+ Kč', '{n} cocktails from {lo} Kč'),
  faq=lambda v: [
   ('How much is a cocktail at Lost & Found?',
    f'Cocktails cost {v["c_lo"]}–{v["c_hi"]} Kč. Classics like Mojito, Negroni or Margarita are {v["k_lo"]}–{v["k_hi"]} Kč, signature cocktails {v["s_lo"]}–{v["s_hi"]} Kč, alcohol-free cocktails {v["n_lo"]}–{v["n_hi"]} Kč.'),
   ('What are the signature cocktails?', f"{v['sig']} and more — {v['n_sig']} house creations you won't find anywhere else in Prague."),
   ('How strong are the cocktails?', 'Every drink on the menu is marked with a strength scale: 💪 light, 💪💪 medium, 💪💪💪 strong, plus 0.0% for alcohol-free.'),
   ('How much is a hookah?', f'Every hookah costs {v["hook"]} Kč, whichever blend you choose.'),
   ('Do you serve food?', f'Yes — pizza from {v["pz"]} Kč, quesadillas from {v["qs"]} Kč, nachos, nuts and chips.'),
   ('Do you have alcohol-free drinks?', f'Yes: 0.0% cocktails such as Virgin Colada, alcohol-free Gin Tonic and Mojito, plus homemade lemonades from {v["lem"]} Kč.'),
   ('Can I pay by card?', 'Yes, we accept card and cash.')]),
 'cz': dict(
  src='cs/index.html', dst='cs/menu/index.html', home='/cs/', url='https://lostfoundcz.com/cs/menu/', inlang='cs',
  intro={
   'cat-halloween': 'Halloweenské koktejly a panáky na omezenou dobu — celý listopad.',
   'cat-signature': 'Autorské výtvory našich barmanů — jinde v Praze je neochutnáte.',
   'cat-classic': 'Všechny klasiky: Espresso Martini, Negroni, Mojito, Mai Tai, Margarita, Old Fashioned a další.',
   'cat-wine': 'Spritzy, Mimosa a koktejly s vínem.',
   'cat-shots': 'Autorské panáky a sety panáků pro celý stůl.',
   'cat-hookah': 'Prémiová vodní dýmka, jedna cena za každou směs. <a href="/cs/hookah/">Více o našem hookah lounge →</a>',
   'cat-nonalco': 'Nealkoholické koktejly 0,0 % a domácí limonády.',
   'cat-food': 'Pizza a quesadilly z naší kuchyně, k tomu nachos, ořechy a chipsy.'},
  facts=lambda v: f'🍸 Autorské koktejly od {v["s_lo"]} Kč · 🌿 Vodní dýmka {v["hook"]} Kč · 🍕 Pizza a quesadilly · 0,0 % nealko koktejly · 💳 Karta i hotovost',
  finder='🍹 Najít drink', photos='📸 Celé menu (fotky)', nav_label='Kategorie menu',
  count_re=(r'\d+ koktejlů od \d+ Kč', '{n} koktejlů od {lo} Kč'),
  faq=lambda v: [
   ('Kolik stojí koktejl v Lost & Found?',
    f'Koktejly stojí {v["c_lo"]}–{v["c_hi"]} Kč. Klasiky jako Mojito, Negroni nebo Margarita {v["k_lo"]}–{v["k_hi"]} Kč, autorské koktejly {v["s_lo"]}–{v["s_hi"]} Kč, nealkoholické koktejly {v["n_lo"]}–{v["n_hi"]} Kč.'),
   ('Jaké máte autorské koktejly?', f"{v['sig']} a další — {v['n_sig']} autorských drinků, které jinde v Praze nenajdete."),
   ('Jak silné jsou koktejly?', 'Každý drink v menu má označenou sílu: 💪 lehký, 💪💪 střední, 💪💪💪 silný, 0,0 % pro nealko.'),
   ('Kolik stojí vodní dýmka?', f'Každá vodní dýmka stojí {v["hook"]} Kč, ať si vyberete jakoukoli směs.'),
   ('Podáváte jídlo?', f'Ano — pizza od {v["pz"]} Kč, quesadilly od {v["qs"]} Kč, nachos, ořechy a chipsy.'),
   ('Máte nealkoholické nápoje?', f'Ano: koktejly 0,0 % jako Virgin Colada, nealko Gin Tonic a Mojito, plus domácí limonády od {v["lem"]} Kč.'),
   ('Můžu platit kartou?', 'Ano, přijímáme kartu i hotovost.')]),
}


def txt(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s)).strip()


def nums(p):
    return [int(x) for x in re.findall(r'\d+', p or '')]


def rng(items):
    v = [n for i in items for n in nums(i['price'])]
    return (min(v), max(v)) if v else (0, 0)


def parse(src):
    s = open(os.path.join(ROOT, src), encoding='utf-8').read()
    cats = []
    for m in re.finditer(r'<details class="menu-cat([^"]*)"[^>]*id="([^"]+)">\s*<summary[^>]*>(.*?)</summary>(.*?)</details>', s, re.S):
        extra, cid, summ, body = m.groups()
        if cid not in ANCHORS:
            continue
        title = re.search(r'<span class="cat-title">(.*?)</span>', summ).group(1).strip()
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


def values(cats):
    by = {c['id']: c['items'] for c in cats}
    g = lambda k: by.get(k, [])
    sig, cla, wine, food, na_all = g('cat-signature'), g('cat-classic'), g('cat-wine'), g('cat-food'), g('cat-nonalco')
    na = [i for i in na_all if '0.0' in i['name'] or '0,0' in i['name']]
    lem = [i for i in na_all if re.search(r'(?i)lemonade|limonád', txt(i['name']))]
    have = [txt(i['name']) for i in sig]
    v = dict(n=len(sig) + len(cla) + len(wine), n_sig=len(sig),
             sig=', '.join([n for n in FEATURED if n in have] or have[:6]),
             hook=rng(g('cat-hookah'))[0],
             pz=rng([i for i in food if txt(i['name']).startswith('Pizza')])[0],
             qs=rng([i for i in food if txt(i['name']).startswith('Quesadill')])[0],
             lem=rng(lem)[0])
    v['c_lo'], v['c_hi'] = rng(sig + cla + wine); v['lo'] = v['c_lo']
    v['s_lo'], v['s_hi'] = rng(sig); v['k_lo'], v['k_hi'] = rng(cla); v['n_lo'], v['n_hi'] = rng(na)
    return v


def block(p, name, content, fallback):
    """Replace <!-- menu:NAME:start --> ... end, or on first run the span returned by fallback(p)."""
    S, E = f'<!-- menu:{name}:start -->', f'<!-- menu:{name}:end -->'
    if S in p:
        a, b = p.index(S), p.index(E) + len(E)
    else:
        a, b = fallback(p)
    return p[:a] + S + '\n' + content + '\n  ' + E + p[b:]


def sync(L):
    cats, legend = parse(L['src'])
    v = values(cats)
    dst = os.path.join(ROOT, L['dst'])
    p = open(dst, encoding='utf-8').read()

    # top block: facts line + buttons + sticky category bar
    links = ''.join((f'<a class="hw-only" href="#{ANCHORS[c["id"]]}">' if c['seasonal'] else f'<a href="#{ANCHORS[c["id"]]}">') + c['title'] + '</a>' for c in cats)
    top = (f'  <p class="facts-line">{L["facts"](v)}</p>\n'
           f'  <div class="btns menu-links"><a class="btn btn-g" href="{L["home"]}#finder">{L["finder"]}</a>'
           f'<a class="btn btn-g" href="{L["home"]}#menu-photos">{L["photos"]}</a></div>\n'
           f'  <nav class="cat-nav" aria-label="{L["nav_label"]}">{links}</nav>')

    def top_fb(p):
        a = p.index('<ul class="facts">')
        b = p.index('</ul>', a) + len('</ul>')
        m = re.compile(r'\s*<div class="btns menu-links">.*?</div>', re.S).match(p, b)
        if m: b = m.end()
        return a, b
    p = block(p, 'top', top, top_fb)

    # menu body
    out = ['  ' + legend]
    for c in cats:
        lis = []
        for i in c['items']:
            al = f' <em class="al" title="{i["tip"]}">({i["allerg"]})</em>' if i['allerg'] else ''
            pr = f' <span>{i["price"]} Kč</span>' if i['price'] else ''
            note = f'<small class="note">{i["note"]}</small>' if i['note'] else ''
            lis.append(f'    <li><b>{i["name"]}{al}{i["scale"]}{pr}</b><small>{i["desc"]}</small>{note}</li>')
        sec = (f'  <h2 id="{ANCHORS[c["id"]]}">{c["title"]}</h2>\n  <p>{L["intro"][c["id"]]}</p>\n'
               f'  <ul class="items">\n' + '\n'.join(lis) + '\n  </ul>')
        out.append(f'  <div class="hw-only">\n{sec}\n  </div>' if c['seasonal'] else sec)

    def body_fb(p):
        f = p.index('<!-- menu:top:end -->')
        a = min(i for i in (p.find('<div class="lf-legend">', f), p.find('<div class="hw-only">', f), p.find('<h2 id=', f)) if i > 0)
        return a, p.index('<p style="margin-top:22px">')
    p = block(p, 'body', '\n'.join(out), body_fb)
    p = re.sub(r'(<!-- menu:body:end -->)\s*', r'\1\n  ', p)

    # FAQ
    qa = L['faq'](v)
    dl = '  <dl class="faq">\n' + ''.join(f'    <dt>{html.escape(q, quote=False)}</dt>\n    <dd>{html.escape(a, quote=False)}</dd>\n' for q, a in qa) + '  </dl>'
    p = block(p, 'faq', dl, lambda p: (p.index('<dl class="faq">'), p.index('</dl>') + 5))
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}, ensure_ascii=False)
    p = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "FAQPage".*?</script>',
               lambda m: '<script type="application/ld+json">' + faq_ld + '</script>', p, count=1, flags=re.S)

    # Menu JSON-LD (evergreen: seasonal categories excluded)
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
        secs.append({"@type": "MenuSection", "name": re.sub(r'^[^\w]+', '', txt(c['title'])), "hasMenuItem": its})
    menu_ld = json.dumps({"@context": "https://schema.org", "@type": "Menu", "name": "Lost & Found Bar Prague — Menu",
                          "inLanguage": L['inlang'], "hasMenuSection": secs, "url": L['url']}, ensure_ascii=False)
    p = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "Menu".*?</script>',
               lambda m: '<script type="application/ld+json">' + menu_ld + '</script>', p, count=1, flags=re.S)

    rx, fmt = L['count_re']
    p = re.sub(rx, fmt.format(**v), p)
    open(dst, 'w', encoding='utf-8').write(p)
    print(f'{L["dst"]} synced:', sum(len(c['items']) for c in cats), 'items in', len(cats), 'categories')


def main():
    for L in LANGS.values():
        if os.path.exists(os.path.join(ROOT, L['dst'])):
            sync(L)


if __name__ == '__main__':
    main()
