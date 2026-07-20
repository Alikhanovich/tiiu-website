# TIIU Website — Test paketi

To'liq qamrovli avtomatlashtirilgan test to'plami: **Django backend (pytest)** + **Playwright E2E**.

## Nima qamrab olingan

| Fayl | Testlar | Nima tekshiriladi |
|------|---------|-------------------|
| `tests/test_models.py` | 21 | 28 model: `__str__`, slug avtogeneratsiya + unikallik, default qiymatlar, ordering, `SiteSettings` singleton |
| `tests/test_public_views.py` | 49 | 20+ public route 200, 13 detail route 404, kontakt forma (valid/invalid/limit) |
| `tests/test_panel_auth.py` | 78 | Login (to'g'ri/xato/non-staff), logout, me, 23 endpoint × 3 rol (anonim 403 / user 403 / staff 200) |
| `tests/test_panel_crud.py` | ~40 | Har resurs uchun CREATE / LIST (pagination) / UPDATE / DELETE / 404 |
| `tests/test_security.py` | ~12 | Buzilgan JSON, metod cheklovi, pk manipulyatsiya, xabar sizib chiqmasligi |
| `e2e/tests/public.spec.js` | 13 | Real brauzerda public sahifalar + kontakt forma |
| `e2e/tests/panel.spec.js` | 13 | Login oqimi, navigatsiya, CRUD (brauzer sessiyasida CSRF bilan), auth 403 |

**Jami: 189 backend test o'tadi + 26 E2E test.**

## 1. Backend testlar (tez, DB kerak emas — SQLite xotirada)

```bash
# O'rnatish
pip install -r requirements-dev.txt

# Barcha testlar
pytest

# Faqat bitta fayl
pytest tests/test_panel_auth.py

# Qamrov hisoboti bilan
pytest --cov=main --cov=panel --cov-report=term-missing

# Batafsil chiqish
pytest -v
```

## 2. E2E testlar (real brauzer + dev server)

```bash
cd e2e
npm install
npx playwright install chromium   # brauzerni bir marta yuklash

# Ishga tushirish (Django serverni avtomatik ko'taradi)
npm test

# Ko'rinadigan brauzerda (debug uchun)
npm run test:headed

# Interaktiv UI rejim
npm run test:ui

# HTML hisobot
npm run report
```

E2E `global-setup.js` avtomatik ravishda `e2e_admin` / `e2e-Pass-123!` staff foydalanuvchisini yaratadi va Django dev-serverni `127.0.0.1:8000` da ishga tushiradi.

---

## ⚠️ Testlar topgan HAQIQIY bug'lar

Test paketi kodingizda **3 ta real xatolikni** aniqladi. Ular `xfail` (kutilgan muvaffaqiyatsizlik) sifatida belgilangan — tuzatgandan so'ng ular avtomatik "o'tgan"ga aylanadi (`strict=True`), shuning uchun tuzatishni unutmasligingiz kafolatlanadi.

### 1. Konferensiya panel orqali qo'shilmaydi
**Fayl:** `panel/views.py` → `api_conferences`
**Muammo:** `start_date` (bu `DateTimeField`) uchun `parse_date()` ishlatilgan. Frontend `datetime-local` (`2026-10-01T09:00`) yuboradi, `parse_date` bunday qiymatni `None` qaytaradi → `NOT NULL constraint failed`.
**Yechim:** `parse_date` o'rniga `parse_datetime` ishlatish:
```python
from django.utils.dateparse import parse_datetime
if d.get('start_date'): o.start_date = parse_datetime(d['start_date'])
if d.get('end_date'):   o.end_date   = parse_datetime(d['end_date'])
```
(Xuddi shu tekshiruvni boshqa DateTimeField'li endpointlarda ham qiling: events, contests deadline, va h.k.)

### 2. Kelgan xabarni o'chirib bo'lmaydi
**Fayl:** `panel/views.py` → `api_message_detail`
**Muammo:** Faqat `POST` (status yangilash) qo'llab-quvvatlanadi, `DELETE` handler'i yo'q. Panel'da xabarni o'chirish tugmasi ishlamaydi.
**Yechim:** view boshiga qo'shing:
```python
if request.method == 'DELETE':
    o.delete()
    return JsonResponse({'success': True})
```

### 3. Login buzilgan JSON'da 500 beradi
**Fayl:** `panel/views.py` → `api_login`
**Muammo:** `json.loads(request.body)` `try/except`siz. Noto'g'ri formatdagi so'rov ishlov berilmagan istisno (500) beradi.
**Yechim:**
```python
try:
    d = json.loads(request.body)
except (ValueError, json.JSONDecodeError):
    return JsonResponse({'success': False, 'error': "Noto'g'ri so'rov"}, status=400)
```

Uchala tuzatishdan keyin:
```bash
# xfail testlarni oddiy testga aylantiring: @pytest.mark.xfail dekoratorlarini olib tashlang
pytest tests/test_panel_crud.py tests/test_security.py
```
