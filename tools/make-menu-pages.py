#!/usr/bin/env python3
"""(Re)create the localized standalone menu pages from the EN template menu/index.html.

  menu/index.html (EN, template) -> cs/menu/, de/menu/, ua/menu/
Static texts (head, header nav, language switcher, footer, headings) come from
STATIC below; the dynamic menu/FAQ parts are filled by sync-menu-page.py,
which this script runs at the end. Use when the template layout changes.
"""
import re, os, runpy
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = 'https://lostfoundcz.com'
PAGES = {'en': '/menu/', 'cs': '/cs/menu/', 'de': '/de/menu/', 'uk': '/ua/menu/'}
HOME = {'en': '/', 'cs': '/cs/', 'de': '/de/', 'uk': '/ua/'}
FLAG = {
 'en': '<svg viewBox="0 0 60 30" width="18" height="12" aria-hidden="true"><path d="M0 0v30h60V0z" fill="#012169"/><path d="M0 0l60 30m0-30L0 30" stroke="#fff" stroke-width="6"/><path d="M0 0l60 30m0-30L0 30" stroke="#C8102E" stroke-width="3"/><path d="M30 0v30M0 15h60" stroke="#fff" stroke-width="10"/><path d="M30 0v30M0 15h60" stroke="#C8102E" stroke-width="6"/></svg>',
 'cs': '<svg viewBox="0 0 60 40" width="18" height="12" aria-hidden="true"><path fill="#fff" d="M0 0h60v20H0z"/><path fill="#D7141A" d="M0 20h60v20H0z"/><path fill="#11457E" d="M0 0l30 20L0 40z"/></svg>',
 'de': '<svg viewBox="0 0 5 3" width="18" height="12" aria-hidden="true"><rect width="5" height="3" fill="#000"/><rect width="5" height="2" y="1" fill="#D00"/><rect width="5" height="1" y="2" fill="#FFCE00"/></svg>',
 'uk': '<svg viewBox="0 0 60 40" width="18" height="12" aria-hidden="true"><rect width="60" height="20" fill="#0057B7"/><rect width="60" height="20" y="20" fill="#FFD700"/></svg>'}
CODE = {'en': 'EN', 'cs': 'CZ', 'de': 'DE', 'uk': 'UA'}

STATIC = {
 'cs': dict(lang='cs', locale='cs_CZ', title='Menu a ceny — Lost &amp; Found Bar Prague',
  desc='Kompletní koktejlové menu s cenami: 60 koktejlů od 165 Kč, autorské drinky, spritzy, panáky, vodní dýmka 535 Kč, nealko nápoje a pizza. Žitná 11, Praha 1.',
  nav=[('/cs/menu/', 'Menu'), ('/cs/hookah/', 'Vodní dýmka'), ('/halloween/', 'Halloween'), ('/cs/#events', 'Soukromé akce'), ('/cs/#visit', 'Kontakt')],
  h1='Koktejlové menu a ceny',
  lead='Kompletní nápojové menu a jídlo v Lost &amp; Found — koktejlovém baru a hookah lounge v Žitné ulici na Praze 1, pár minut chůze od Václavského náměstí. 60 koktejlů od 165 Kč, autorské panáky, prémiová vodní dýmka, nealko drinky a pizza.',
  note='Ceny v Kč, mohou se změnit. Fotky tištěného menu najdete na <a href="/cs/#menu-photos">hlavní stránce</a>.',
  faq_h='Časté dotazy k menu', reserve='Rezervovat stůl', directions='Navigovat',
  f1='Lost &amp; Found Bar Prague — koktejlový bar a hookah lounge', open='Otevřeno: Ne–Út 18–00 | St–Čt 17–01 | Pá–So 17–03',
  flinks=[('/cs/', 'Domů'), ('/cs/menu/', 'Menu'), ('/cs/hookah/', 'Vodní dýmka'), ('/halloween/', 'Halloween'), ('/cs/privacy.html', 'Ochrana soukromí')]),
 'de': dict(lang='de', locale='de_DE', title='Karte &amp; Preise — Lost &amp; Found Bar Prague',
  desc='Komplette Cocktailkarte mit Preisen: 60 Cocktails ab 165 Kč, Signature-Drinks, Spritz, Shots, Shisha 535 Kč, alkoholfreie Drinks und Pizza. Žitná 11, Prag 1.',
  nav=[('/de/menu/', 'Karte'), ('/de/hookah/', 'Shisha'), ('/halloween/', 'Halloween'), ('/de/#events', 'Private Events'), ('/de/#visit', 'Anfahrt')],
  h1='Cocktailkarte &amp; Preise',
  lead='Die komplette Getränke- und Speisekarte der Lost &amp; Found Bar — Cocktailbar und Shisha-Lounge in der Žitná-Straße in Prag 1, wenige Gehminuten vom Wenzelsplatz. 60 Cocktails ab 165 Kč, Signature-Shots, Premium-Shisha, alkoholfreie Drinks und Pizza.',
  note='Preise in CZK, Änderungen vorbehalten. Fotos der gedruckten Karte gibt es auf der <a href="/de/#menu-photos">Startseite</a>.',
  faq_h='Häufige Fragen zur Karte', reserve='Tisch reservieren', directions='Route planen',
  f1='Lost &amp; Found Bar Prague — Cocktailbar &amp; Shisha-Lounge', open='Geöffnet: So–Di 18–00 | Mi–Do 17–01 | Fr–Sa 17–03',
  flinks=[('/de/', 'Startseite'), ('/de/menu/', 'Karte'), ('/de/hookah/', 'Shisha'), ('/halloween/', 'Halloween'), ('/privacy.html', 'Datenschutz')]),
 'uk': dict(lang='uk', locale='uk_UA', title='Меню та ціни — Lost &amp; Found Bar Prague',
  desc='Повне коктейльне меню з цінами: 60 коктейлів від 165 Kč, авторські напої, спритци, шоти, кальян 535 Kč, безалкогольні напої та піца. Žitná 11, Прага 1.',
  nav=[('/ua/menu/', 'Меню'), ('/hookah/', 'Кальян'), ('/halloween/', 'Halloween'), ('/ua/#events', 'Приватні події'), ('/ua/#visit', 'Як дістатися')],
  h1='Коктейльне меню та ціни',
  lead='Повне меню напоїв і страв Lost &amp; Found — коктейль-бару та кальянного лаунжу на вулиці Žitná у Празі 1, за кілька хвилин пішки від Вацлавської площі. 60 коктейлів від 165 Kč, авторські шоти, преміальний кальян, безалкогольні напої та піца.',
  note='Ціни в CZK, можуть змінюватися. Фото друкованого меню — на <a href="/ua/#menu-photos">головній сторінці</a>.',
  faq_h='Питання про меню', reserve='Забронювати стіл', directions='Прокласти маршрут',
  f1='Lost &amp; Found Bar Prague — коктейль-бар і кальянний лаунж', open='Відчинено: Нд–Вт 18–00 | Ср–Чт 17–01 | Пт–Сб 17–03',
  flinks=[('/ua/', 'Головна'), ('/ua/menu/', 'Меню'), ('/hookah/', 'Кальян'), ('/halloween/', 'Halloween'), ('/privacy.html', 'Конфіденційність')]),
}

def switcher(cur):
    return ('<div class="mlang" aria-label="Language">' + ''.join(
        f'<a href="{PAGES[l]}" hreflang="{"cs" if l=="cs" else l}"' + (' class="on" aria-current="true"' if l == cur else '') + f'>{FLAG[l]}{CODE[l]}</a>'
        for l in PAGES) + '</div>')

def hreflang():
    return ''.join(f'<link rel="alternate" hreflang="{l}" href="{B}{PAGES[l]}">\n' for l in PAGES) + \
           f'<link rel="alternate" hreflang="x-default" href="{B}/menu/">\n'

CSS = ('.mlang{display:flex;gap:6px;flex-wrap:wrap}.mlang a{display:inline-flex;align-items:center;gap:6px;padding:5px 10px;border:1px solid var(--line);'
       'border-radius:8px;font-size:12px;font-weight:700;letter-spacing:.04em;color:var(--muted);text-decoration:none}'
       '.mlang a.on{color:#fff;border-color:rgba(200,85,181,.6);background:rgba(200,85,181,.14)}.mlang a:hover{color:#fff}\n')

def fix_template(p):
    """Normalize the EN template: hreflang x4, switcher in header, banner targets -> menu pages."""
    p = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]+">\n', '', p)
    p = p.replace('<link rel="canonical" href="https://lostfoundcz.com/menu/">\n', '<link rel="canonical" href="https://lostfoundcz.com/menu/">\n' + hreflang(), 1)
    p = re.sub(r'\n  <div class="mlang".*?</div>', '', p, flags=re.S)
    p = p.replace('\n</div></header>', '\n  ' + switcher('en') + '\n</div></header>', 1)
    if '.mlang{' not in p:
        p = p.replace('</style>', CSS + '</style>', 1)
    p = p.replace("t={h:'/de/',", "t={h:'/de/menu/',")
    p = re.sub(r'<a href="/cs/(?:menu/)?">Česky</a> · <a href="/de/(?:menu/)?">Deutsch</a>(?: · <a href="/ua/menu/">Українська</a>)*', '<a href="/cs/menu/">Česky</a> · <a href="/de/menu/">Deutsch</a> · <a href="/ua/menu/">Українська</a>', p)
    return p

def localize(en, l):
    S = STATIC[l]; p = en; url = B + PAGES[l]
    p = p.replace('<html lang="en">', f'<html lang="{S["lang"]}">', 1)
    p = re.sub(r'<title>.*?</title>', f'<title>{S["title"]}</title>', p, count=1)
    p = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{S["title"]}">', p, count=1)
    p = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{S["desc"]}">', p, count=1)
    p = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{S["desc"]}">', p, count=1)
    p = p.replace('<link rel="canonical" href="https://lostfoundcz.com/menu/">', f'<link rel="canonical" href="{url}">', 1)
    p = p.replace('<meta property="og:url" content="https://lostfoundcz.com/menu/">', f'<meta property="og:url" content="{url}">', 1)
    p = p.replace('<meta property="og:locale" content="en_US">', f'<meta property="og:locale" content="{S["locale"]}">', 1)
    p = p.replace('<a class="logo" href="/">', f'<a class="logo" href="{HOME[l]}">', 1)
    nav = ''.join((f'<a class="hw-only" href="{h}">{t}</a>' if 'halloween' in h else
                   f'<a href="{h}"' + (' aria-current="page"' if h == PAGES[l] else '') + f'>{t}</a>') for h, t in S['nav'])
    p = re.sub(r'<nav>.*?</nav>', f'<nav>{nav}</nav>', p, count=1, flags=re.S)
    p = p.replace(switcher('en'), switcher(l), 1)
    p = re.sub(r'<div class="crumbs"><a href="/">', f'<div class="crumbs"><a href="{HOME[l]}">', p, count=1)
    p = re.sub(r'<h1>.*?</h1>', f'<h1>{S["h1"]}</h1>', p, count=1)
    p = re.sub(r'<p class="lead">.*?</p>', f'<p class="lead">{S["lead"]}</p>', p, count=1, flags=re.S)
    p = re.sub(r'<p style="margin-top:22px">.*?</p>', f'<p style="margin-top:22px">{S["note"]}</p>', p, count=1, flags=re.S)
    p = re.sub(r'<h2 id="faq">.*?</h2>', f'<h2 id="faq">{S["faq_h"]}</h2>', p, count=1)
    p = p.replace('rel="noopener">Reserve a table</a>', f'rel="noopener">{S["reserve"]}</a>', 1)
    p = p.replace('">Get directions</a>', f'">{S["directions"]}</a>', 1)
    p = p.replace('Lost &amp; Found Bar Prague — Cocktail Bar &amp; Hookah Lounge<br>', S['f1'] + '<br>', 1)
    p = re.sub(r'Open: Sun–Tue[^<]*<br>', S['open'] + '<br>', p, count=1)
    others = ' · '.join(f'<a href="{PAGES[o]}">{n}</a>' for o, n in (('en', 'English'), ('cs', 'Česky'), ('de', 'Deutsch'), ('uk', 'Українська')) if o != l)
    fl = ' · '.join(f'<a href="{h}">{t}</a>' for h, t in S['flinks'][:-1]) + ' · ' + others + f' · <a href="{S["flinks"][-1][0]}">{S["flinks"][-1][1]}</a>'
    p = re.sub(r'(<footer><div class="wrap">.*?<br>\s*.*?<br>\s*.*?<br>\s*).*?(\n</div></footer>)', lambda m: m.group(1) + fl + m.group(2), p, count=1, flags=re.S)
    p = p.replace('"item": "https://lostfoundcz.com/"}', f'"item": "{B}{HOME[l]}"}}', 1)
    p = p.replace('"item": "https://lostfoundcz.com/menu/"}', f'"item": "{url}"}}', 1)
    return p

def main():
    tp = os.path.join(ROOT, 'menu', 'index.html')
    en = fix_template(open(tp, encoding='utf-8').read())
    open(tp, 'w', encoding='utf-8').write(en)
    for l, d in (('cs', 'cs/menu'), ('de', 'de/menu'), ('uk', 'ua/menu')):
        os.makedirs(os.path.join(ROOT, d), exist_ok=True)
        open(os.path.join(ROOT, d, 'index.html'), 'w', encoding='utf-8').write(localize(en, l))
        print('made', d + '/index.html')
    runpy.run_path(os.path.join(ROOT, 'tools', 'sync-menu-page.py'), run_name='__main__')

if __name__ == '__main__':
    main()
