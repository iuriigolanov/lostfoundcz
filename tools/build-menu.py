#!/usr/bin/env python3
"""Single-source menu generator.

Edit tools/menu-data.json (prices, descriptions EN/CS/DE, optional "note"),
then run:  python tools/build-menu.py
It regenerates — in index.html, cs/index.html, de/index.html — the menu
accordion (all 6 categories), the Menu JSON-LD, and the drink finder DB,
keeping all three languages and all three surfaces in sync.

"2x" in any description is auto-highlighted as a double-portion perk.
An optional per-item "note" (an enticing one-liner, per language) is shown
under the ingredients in the accordion.
"""
import re,json,os,sys

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,'tools','menu-data.json')
FILES={'en':'index.html','cz':'cs/index.html','de':'de/index.html'}

def esc_plain(s):
    # for JSON-LD / finder: strip html entities back to plain text
    return (s.replace('&amp;','&').replace('&#x27;',"'"))

def hl(desc):
    # highlight 2x as a perk badge (accordion only)
    return re.sub(r'(?<![\w])2x(?=[ \b])', '<span class="mi-x2">2×</span>', desc)

def mi_html(item,lang):
    name=item['name']; price=item.get('price')
    desc=hl(item['desc'][lang])
    note=item.get('note',{}).get(lang) if isinstance(item.get('note'),dict) else None
    allerg=item.get('allergens')
    nm=f'<span class="mi-name">{name}</span>'
    if allerg: nm+=f'<span class="mi-allerg" title="Allergens">({allerg})</span>'
    head=nm+'<span class="mi-dots"></span>'
    if price not in (None,''): head+=f'<span class="mi-price">{price}</span>'
    body=f'        <div class="mi-head">{head}</div>\n        <div class="mi-desc">{desc}</div>\n'
    if note: body+=f'        <div class="mi-note">{note}</div>\n'
    return '      <div class="mi">\n'+body+'      </div>\n'

def build_accordion(data,lang):
    out={}
    for c in data['categories']:
        out[c['id']]=''.join(mi_html(it,lang) for it in c['items'])
    return out

def build_jsonld(data):
    secs=[]
    for c in data['categories']:
        mis=[]
        for it in c['items']:
            price=it.get('price')
            if c['flat'] and (price in (None,'')):
                price=re.sub(r'[^0-9]','',c['flat'])  # hookah flat -> number
            mis.append({"@type":"MenuItem","name":esc_plain(it['name']),
                        "description":esc_plain(it['desc']['en']),
                        "offers":{"@type":"Offer","price":price,"priceCurrency":"CZK"}})
        secs.append({"@type":"MenuSection","name":esc_plain(c['name']['en']),"hasMenuItem":mis})
    menu={"@context":"https://schema.org","@type":"Menu","name":"Lost & Found Bar Prague — Full Menu",
          "inLanguage":"en","hasMenuSection":secs,"url":"https://lostfoundcz.com/#menu"}
    return '<script type="application/ld+json">'+json.dumps(menu,ensure_ascii=False,separators=(',',':'))+'</script>'

def build_finder(data):
    lines=['  const DRINKS = [']
    for c in data['categories']:
        grp=[it for it in c['items'] if 'finder' in it]
        if not grp: continue
        lines.append('  // '+esc_plain(c['name']['en']))
        for it in grp:
            f=it['finder']
            fl='['+','.join('"%s"'%x for x in f['fl'])+']'
            vb='['+','.join('"%s"'%x for x in f['vb'])+']'
            lines.append('  {n:"%s",p:"%s",d:"%s",sp:"%s",fl:%s,sw:%d,st:%d,vb:%s},'%(
                f['name'],it.get('price',''),f['d'],f['sp'],fl,f['sw'],f['st'],vb))
    lines.append('  ];')
    return '\n'.join(lines)

CSS_RULE='.mi-x2{display:inline-block;font-weight:800;color:#06060a;background:linear-gradient(90deg,var(--violet,#c855b5),var(--cyan,#3fc5f0));padding:0 5px;border-radius:5px;font-size:12px;line-height:1.5;vertical-align:1px}.mi-note{margin-top:4px;font-style:italic;font-size:12.5px;color:var(--cyan,#3fc5f0);opacity:.92}'

ALLERG_CSS='.mi-allerg{color:var(--muted,#9aa);font-size:11px;font-weight:600;margin-left:5px;vertical-align:1px}.allergen-legend{max-width:820px;margin:14px auto 0;border:1px solid rgba(255,255,255,.08);border-radius:12px;background:rgba(255,255,255,.02)}.allergen-legend summary{cursor:pointer;list-style:none;padding:12px 16px;color:var(--muted,#9aa);font-size:12.5px;letter-spacing:.04em}.allergen-legend summary::-webkit-details-marker{display:none}.allergen-legend summary::before{content:"▸ ";color:var(--violet,#c855b5)}.allergen-legend[open] summary::before{content:"▾ "}.allergen-legend .al-body{padding:0 16px 14px}.allergen-legend ol{columns:2;column-gap:26px;margin:6px 0 0;padding-left:18px;font-size:12.5px;color:var(--ink,#e8e8ee)}.allergen-legend li{margin:3px 0;break-inside:avoid}.allergen-legend .al-foot{margin-top:10px;font-size:11.5px;color:var(--muted,#9aa)}@media(max-width:560px){.allergen-legend ol{columns:1}}'

# EU 1169/2011 Annex II — the 14 declarable allergens
ALLERG_14={
 'en':['Cereals containing gluten','Crustaceans','Eggs','Fish','Peanuts','Soybeans','Milk (lactose)','Tree nuts','Celery','Mustard','Sesame','Sulphur dioxide &amp; sulphites','Lupin','Molluscs'],
 'cz':['Obiloviny obsahující lepek','Korýši','Vejce','Ryby','Arašídy','Sója','Mléko (laktóza)','Skořápkové plody (ořechy)','Celer','Hořčice','Sezam','Oxid siřičitý a siřičitany','Vlčí bob (lupina)','Měkkýši'],
 'de':['Glutenhaltiges Getreide','Krebstiere','Eier','Fisch','Erdnüsse','Soja','Milch (Laktose)','Schalenfrüchte (Nüsse)','Sellerie','Senf','Sesam','Schwefeldioxid und Sulfite','Lupinen','Weichtiere'],
}
ALLERG_L={
 'en':('Allergens — what the numbers mean','The number(s) after an item show its declarable allergens. Drinks may contain traces of others. <a href="/seznam-alergenu-a4.pdf" target="_blank" rel="noopener" style="color:var(--cyan,#3fc5f0);text-decoration:underline">Full allergen list (PDF)</a>'),
 'cz':('Alergeny — co znamenají čísla','Čísla u položky označují obsažené alergeny. Nápoje mohou obsahovat stopy dalších. <a href="/seznam-alergenu-a4.pdf" target="_blank" rel="noopener" style="color:var(--cyan,#3fc5f0);text-decoration:underline">Úplný seznam alergenů (PDF)</a>'),
 'de':('Allergene — was die Nummern bedeuten','Die Nummer(n) bei einem Artikel zeigen die kennzeichnungspflichtigen Allergene. Getränke können Spuren weiterer enthalten. <a href="/seznam-alergenu-a4.pdf" target="_blank" rel="noopener" style="color:var(--cyan,#3fc5f0);text-decoration:underline">Vollständige Allergenliste (PDF)</a>'),
}

def build_legend(lang):
    title,foot=ALLERG_L[lang]
    items=''.join('<li>%d. %s</li>'%(i+1,a) for i,a in enumerate(ALLERG_14[lang]))
    return ('<details class="allergen-legend"><summary>'+title+'</summary>'
            '<div class="al-body"><ol>'+items+'</ol>'
            '<div class="al-foot">'+foot+'</div></div></details>')

def ensure_css(h):
    if '.mi-allerg{' not in h:
        h=h.replace('</style>', ALLERG_CSS+'</style>',1)
    if '.mi-x2{' in h: return h
    return h.replace('</style>', CSS_RULE+'</style>',1)

def ensure_legend(h,lang):
    leg=build_legend(lang)
    # remove any existing legend, then insert before the menu-photos toggle
    h=re.sub(r'\s*<details class="allergen-legend">.*?</details>','',h,flags=re.S)
    anchor='\n  <details class="menu-photos-toggle">'
    if anchor in h:
        h=h.replace(anchor,'\n  '+leg+anchor,1)
    return h

def main():
    data=json.load(open(DATA,encoding='utf-8'))
    for lang,fname in FILES.items():
        p=os.path.join(ROOT,fname); h=open(p,encoding='utf-8').read()
        acc=build_accordion(data,lang)
        for cid,items in acc.items():
            m=re.search(r'(<details class="menu-cat"[^>]*id="'+cid+r'">.*?<div class="cat-items">\n)(.*?)(\n    </div>\n  </details>)', h, re.S)
            if not m: sys.exit('cat not found: %s in %s'%(cid,fname))
            h=h[:m.start(2)]+items.rstrip('\n')+h[m.end(2):]
        # hookah flat price
        for c in data['categories']:
            if c['flat']:
                h=re.sub(r'(<span class="cat-flat">)[^<]*(</span>)', r'\g<1>'+c['flat']+r'\g<2>', h, count=1)
        # Menu JSON-LD (same on all langs)
        newmenu=build_jsonld(data)
        def repj(mo): return newmenu if '"@type":"Menu"' in mo.group(1) else mo.group(0)
        h=re.sub(r'<script type="application/ld\+json">(.*?)</script>', repj, h, flags=re.S)
        # finder DB (shared)
        h=re.sub(r'  const DRINKS = \[.*?\n  \];', build_finder(data).replace('\\','\\\\'), h, count=1, flags=re.S)
        h=ensure_css(h)
        h=ensure_legend(h,lang)
        open(p,'w',encoding='utf-8').write(h)
        print('built',fname)

if __name__=='__main__':
    main()
