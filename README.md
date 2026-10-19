# Греція 2026

Фотожурнал подорожі 8–17 жовтня: 28 сторінок, 69 фотографій.

Сайт: https://sergejkolesnik.github.io/greece-2026-photo-book/

Статичні файли у `docs/`. Для локального перегляду: `python -m http.server 8000 --directory docs`. Це 28 окремих макетних фотосторінок; усі 69 фото доступні й без JavaScript.

Після оновлення `main` GitHub Pages автоматично публікує каталог `docs`. PDF доступний за посиланням у нижній частині журналу. Фотографії авторські; дозвіл переглядати журнал не означає передачу прав на повторне використання.

Редакційне джерело — `docs/content.json`. Збірка: `python scripts/build_site.py`; PDF: `python scripts/build_pdf.py` (Pillow, reportlab і Segoe UI/Georgia; каталог шрифтів можна задати через `JOURNAL_FONT_DIR`). Перевірка: `python scripts/verify_journal.py --url https://sergejkolesnik.github.io/greece-2026-photo-book/`.

Посторінковий аудит — `PAGE_AUDIT.csv`. Контекст і рішення збережені в PROJECT_CONTEXT.md, PROJECT_STATUS.md і DECISIONS.md; розбір суперечностей Hermes — в EDITORIAL_RECONCILIATION.md. SVG-карта обслуговується самим сайтом, геодані OSM доступні в `docs/map-data/`; атрибуція і методика — MAP_SOURCE.md.
