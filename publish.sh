#!/usr/bin/env bash
# Kontentni productionga chiqarish (bitta buyruq).
#
# Lokal panelda o'qituvchi/yangilik/rasm qo'shgach shuni ishga tushiring:
#     ./publish.sh
#
# U lokal bazadagi butun kontentni fixture'ga eksport qiladi, media rasmlar
# bilan birga git'ga qo'shadi, commit qilib GitHub'ga push qiladi. Render
# avtomatik qayta deploy qilib, productionni yangi kontent bilan to'ldiradi.
set -o errexit
cd "$(dirname "$0")"

echo "1/4  Kontent fixture'ga eksport qilinmoqda..."
python manage.py dumpdata main --indent 2 -o main/fixtures/initial_data.json

echo "2/4  O'zgarishlar (fixture + media) qo'shilmoqda..."
git add main/fixtures/initial_data.json media

echo "3/4  Commit..."
if git diff --cached --quiet; then
  echo "     Hech qanday o'zgarish yo'q — to'xtatildi."
  exit 0
fi
git commit -m "content: kontent yangilandi ($(date +%Y-%m-%d))"

echo "4/4  GitHub'ga push..."
git push origin main

echo "✅  Tayyor. Render qayta deploy qilmoqda — bir-ikki daqiqada production yangilanadi."
