# Lost & Found Bar Prague — сайт

Исходники lostfoundcz.com (GitHub Pages).

## Версии
- `v1.0-base` — базовая версия, 935 отзывов, есть Tripadvisor. Точка отката.

## Как откатиться
    git log --oneline                    # список версий
    git checkout v1.0-base -- index.html # вернуть index.html из версии

## Правила
- Правки — только в отдельной ветке, не в main.
- Перед мержем: git diff + проверка в браузере.
