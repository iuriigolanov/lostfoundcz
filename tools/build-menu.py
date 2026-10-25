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
    head=f'<span class="mi-name">{name}</span><span class="mi-dots"></span>'
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

def ensure_css(h):
    if '.mi-x2{' in h: return h
    # inject once before first </style>
    return h.replace('</style>', CSS_RULE+'</style>',1)

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
        open(p,'w',encoding='utf-8').write(h)
        print('built',fname)

if __name__=='__main__':
    main()
