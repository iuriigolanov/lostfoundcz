# Lost & Found Bar Prague — сайт

Исходники lostfoundcz.com (GitHub Pages).
Репозиторий: https://github.com/iuriigolanov/lostfoundcz

## Версии

| Тег | Что внутри |
|---|---|
| `v1.0-base` | Базовая версия. 935 отзывов, canonical на sites.google.com, картинки в base64. **Чистая точка отката.** |
| `v1.1-seo` | canonical -> lostfoundcz.com, og:image вынесен в файл, 955 отзывов. Страница 2.68 -> 2.05 MB. |

## Откат

    git log --oneline                     # список версий
    git checkout v1.0-base -- index.html  # вернуть index.html из версии
    git checkout v1.1-seo -- index.html

## Рабочий цикл

    git checkout -b имя-задачи   # 1. ветка под задачу
                                 # 2. внести правки
    git diff                     # 3. проверить что изменилось
                                 # 4. открыть index.html в браузере
    git add -A && git commit -m "описание"
    git checkout main
    git merge имя-задачи         # 5. влить, если всё ок
    git push

Не подошло: `git checkout main && git branch -D имя-задачи`

## Важно
- `og-image.png` должен лежать в корне рядом с `index.html` — иначе og:image битый.
- Правки только в ветке, не в main напрямую.

## TODO
- Вынести hero-логотип и 6 фото меню из base64 в файлы (~2 MB, ускорит загрузку)
- Google Search Console + sitemap.xml
