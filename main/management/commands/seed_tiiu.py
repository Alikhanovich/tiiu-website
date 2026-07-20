"""
tiiu.uz saytidan olingan haqiqiy ma'lumotlar bilan bazani to'ldiradi.
Ma'lumotlar DB modellariga yoziladi — ya'ni keyin /panel orqali tahrirlanadi.
Idempotent (update_or_create) — qayta ishga tushirish xavfsiz, dublikat yaratmaydi.

    python manage.py seed_tiiu
"""
from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from main.models import (
    SiteSettings, Faculty, Leadership, Department, Center,
    Teacher, NewsCategory, News, Event,
)


# ── 10 ta ta'lim yo'nalishi (tiiu.uz/educational-directions) ────────────────
DIRECTIONS = [
    ("Iqtisodiyot",
     "Zamonaviy iqtisodiy tahlil, bozor jarayonlari va raqamli ko'nikmalar."),
    ("Moliya va moliyaviy texnologiyalar",
     "Moliyaviy boshqaruv, investitsiya va fintech yechimlari."),
    ("Buxgalteriya hisobi va audit",
     "Hisob yuritish, moliyaviy hisobot va audit amaliyoti."),
    ("Bank ishi",
     "Bank tizimi, kredit siyosati va moliyaviy xizmatlar."),
    ("Axborot tizimlari va texnologiyalari",
     "Dasturlash, ma'lumotlar tahlili va axborot tizimlarini loyihalash."),
    ("Psixologiya",
     "Shaxs psixologiyasi, maslahat va amaliy psixodiagnostika."),
    ("Boshlang'ich ta'lim",
     "Boshlang'ich sinf o'qituvchisini tayyorlash metodikasi."),
    ("Maktabgacha ta'lim",
     "Bolalar rivojlanishi va maktabgacha ta'lim pedagogikasi."),
    ("Jismoniy madaniyat",
     "Sport pedagogikasi, salomatlik va jismoniy tarbiya."),
    ("Filologiya va tillarni o'qitish",
     "Til va adabiyot, chet tillarini o'qitish metodikasi."),
]

SETTINGS = {
    "site_name": "TIIU",
    "site_name_full": "Toshkent ijtimoiy innovatsiya universiteti",
    "founded_year": 2022,           # oliy ta'lim litsenziyasi: 22.11.2022
    "student_count": 2000,          # 2000+ talaba
    "teacher_count": 50,
    "direction_count": 10,          # 10 ta ta'lim yo'nalishi
    "hero_title": "Mustaqil fikr, ijtimoiy ta'sir",
    "hero_subtitle": (
        "Ilg'or ta'lim texnologiyalari asosida ijtimoiy soha va iqtisodiyot "
        "tarmoqlari uchun malakali kadrlar tayyorlaydigan nodavlat oliy ta'lim tashkiloti."
    ),
    "about_text": (
        "Toshkent ijtimoiy innovatsiya universiteti — ijtimoiy soha va iqtisodiyot "
        "tarmoqlari uchun zamonaviy bilim va ko'nikmalarga ega, mas'uliyatni o'z zimmasiga "
        "olishga qodir, mustaqil fikrlaydigan malakali kadrlarni yetishtirib beruvchi "
        "nodavlat oliy ta'lim tashkiloti."
    ),
    "phone1": "+998 78 113 17 17",
    "phone2": "+998 55 506 12 77",
    "email": "info@tiiu.uz",
    "address": "Toshkent sh., Sergeli tumani, Bobur AP, Uzumzor ko'chasi, 37",
    "facebook": "https://facebook.com/tiiu.uz",
    "instagram": "https://instagram.com/tiiu_uz",
    "telegram": "https://t.me/tiiu_universiteti",
    "youtube": "https://youtube.com/@tiiu_uz",
}

# ── Rahbariyat (tiiu.uz/rahbariyat) ─────────────────────────────────────────
LEADERSHIP = [
    dict(full_name="Maxmudov Akbar Abduxamidovich", position="Rektor",
         rank="Dotsent", qualification="Iqtisod fanlari bo'yicha falsafa doktori (PhD)",
         email="rector@tiiu.uz", phone="+998 97 009 79 75",
         reception_days="Seshanba, Payshanba, Juma", reception_time="15:00–16:00", order=1),
    dict(full_name="Nazarov Abdukarim Kusharovich",
         position="Ma'naviy-ma'rifiy ishlar bo'yicha prorektor",
         rank="", qualification="Iqtisod fanlari bo'yicha falsafa doktori (PhD)",
         email="anazarov@tiiu.uz", phone="+998 97 009 79 75",
         reception_days="Dushanba–Juma", reception_time="10:00–15:00", order=2),
    dict(full_name="Ro'ziyev Nasim Ibragimovich",
         position="Moliyaviy resurslarni rejalashtirish bo'limi boshlig'i",
         rank="", qualification="",
         email="roziev@tiiu.uz", phone="+998 97 009 79 75",
         reception_days="Dushanba–Juma", reception_time="10:00–15:00", order=3),
    dict(full_name="Shaxasanova Malika Abduzaxidovna",
         position="Kadrlar bo'yicha inspektor",
         rank="", qualification="",
         email="mshahasanova@tiiu.uz", phone="+998 97 009 79 75",
         reception_days="Dushanba–Juma", reception_time="10:00–15:00", order=4),
]

# ── Kafedralar (tiiu.uz/departments) ────────────────────────────────────────
DEPARTMENTS = [
    dict(name="\"Iqtisodiyot va raqamli texnologiyalar\" kafedrasi",
         head="Bazarov Qahramon Tashtemirovich",
         description="Iqtisodiyot va raqamli texnologiyalar sohasida bilim beruvchi kafedra. "
                     "Mudir — iqtisod fanlari bo'yicha falsafa doktori (PhD), dotsent.", order=1),
    dict(name="\"Pedagogika va psixologiya\" kafedrasi",
         head="Kadyrov Kamoliddin Batyrovich",
         description="Pedagogika va psixologiya yo'nalishlari bo'yicha kafedra. "
                     "Mudir — psixologiya fanlari doktori, professor.", order=2),
]

# ── Markazlar va bo'limlar (tiiu.uz/centers) ────────────────────────────────
CENTERS = [
    dict(name="O'quv-uslubiy bo'lim", icon="📚", head="Ismatullaev Fazliddin Rajabovich",
         head_role="Bo'lim boshlig'i", head_phone="+998 97 009 79 75",
         head_email="fismatullaev@tiiu.uz", work_hours="Dushanba–Juma 10:00–15:00", order=1),
    dict(name="Moliyaviy resurslarni rejalashtirish bo'limi", icon="💰",
         head="Ro'ziyev Nasim Ibragimovich", head_role="Bo'lim boshlig'i",
         head_phone="+998 97 009 79 75", head_email="roziev@tiiu.uz",
         work_hours="Dushanba–Juma 10:00–15:00", order=2),
    dict(name="Axborot texnologiyalari markazi", icon="💻",
         head="Orziqulov Shohruh Ismatullayevich", head_role="Markaz rahbari",
         head_phone="+998 99 842 27 60", head_email="shorziqulov@tiiu.uz",
         work_hours="Dushanba–Juma 10:00–15:00", order=3),
    dict(name="Kadrlar bo'limi", icon="👥", head="Shaxasanova Malika Abduzaxidovna",
         head_role="Inspektor", head_phone="+998 97 009 79 75",
         head_email="mshahasanova@tiiu.uz", work_hours="Dushanba–Juma 10:00–15:00", order=4),
    dict(name="Yoshlar bilan ishlash va talabalar xizmati bo'limi", icon="🎓",
         head="", head_role="Bo'lim", head_phone="+998 97 009 79 75",
         head_email="gboboeva@tiiu.uz", work_hours="Dushanba–Juma 10:00–15:00", order=5),
]

# ── O'qituvchilar (tiiu.uz/departments professor-o'qituvchilari) ────────────
# (dept = tegishli kafedra nomi; FK quyida bog'lanadi)
TEACHERS = [
    dict(full_name="Bazarov Qahramon Tashtemirovich", position="Kafedra mudiri, dotsent",
         dept="\"Iqtisodiyot va raqamli texnologiyalar\" kafedrasi", order=1),
    dict(full_name="Artikov Nodirjon Yakubdjanovich", position="Dotsent",
         dept="\"Iqtisodiyot va raqamli texnologiyalar\" kafedrasi", order=2),
    dict(full_name="Valiyev Burxon", position="Dotsent",
         dept="\"Iqtisodiyot va raqamli texnologiyalar\" kafedrasi", order=3),
    dict(full_name="Butaev Dovlatali Inomovich", position="Dotsent",
         dept="\"Iqtisodiyot va raqamli texnologiyalar\" kafedrasi", order=4),
    dict(full_name="Kadyrov Kamoliddin Batyrovich", position="Kafedra mudiri, professor",
         dept="\"Pedagogika va psixologiya\" kafedrasi", order=5),
    dict(full_name="Soliyeva Dilfuza Abidovna", position="Dotsent",
         dept="\"Pedagogika va psixologiya\" kafedrasi", order=6),
]

# ── Yangiliklar (tiiu.uz/news) ──────────────────────────────────────────────
NEWS = [
    dict(title="Kelajagingizni biz bilan quring",
         short_text="Toshkent ijtimoiy innovatsiya universiteti abituriyentlarni yangi o'quv yiliga taklif etadi.",
         body="Toshkent ijtimoiy innovatsiya universiteti — ijtimoiy soha va iqtisodiyot tarmoqlari "
              "uchun zamonaviy kadrlar tayyorlaydigan nodavlat oliy ta'lim tashkiloti. Universitet "
              "abituriyentlarni hujjat topshirib, kelajagini biz bilan qurishga taklif etadi.",
         is_featured=True),
    dict(title="\"Buxgalteriya hisobi va audit\" yo'nalishi 1-kurs talabalari SHON-SHARAF muzeyiga ekskursiya uyushtirdi",
         short_text="1-kurs talabalari muzeyda fan, ta'lim, madaniyat va sog'liqni saqlash sohalari bilan tanishdilar.",
         body="\"Buxgalteriya hisobi va audit\" yo'nalishi 1-kurs talabalari SHON-SHARAF muzeyiga tashrif "
              "buyurishdi. Talabalar mamlakatimizdagi fan, ta'lim, madaniyat va sog'liqni saqlash sohalari "
              "tarixi bilan yaqindan tanishdilar."),
    dict(title="TIIU talabalari ishtirokida xavfsizlik kuni munosabati bilan profilaktik tadbir o'tkazildi",
         short_text="Universitetda xavfsizlik bo'yicha ma'rifiy profilaktik tadbir tashkil etildi.",
         body="TIIU talabalari ishtirokida xavfsizlik kuni munosabati bilan profilaktik ma'rifiy tadbir "
              "o'tkazildi. Tadbirda xavfsizlik qoidalari va ehtiyotkorlik masalalari muhokama qilindi."),
    dict(title="Profilaktika inspektorlari tomonidan targ'ibot tadbirlari o'tkazildi",
         short_text="Toshkent shahar profilaktika inspektorlari targ'ibot ishlarini olib bordi.",
         body="Toshkent shahar IIBB profilaktika inspektorlari tomonidan universitet talabalari uchun "
              "huquqbuzarliklarning oldini olishga qaratilgan targ'ibot tadbirlari o'tkazildi."),
]

# ── Tadbirlar (tiiu.uz/events) ──────────────────────────────────────────────
EVENTS = [
    dict(title="\"Milliylikka zamonaviy yondashuv!\" — Xon Atlas kuni",
         description="O'zbek milliy madaniyatini targ'ib qilish maqsadida Xon Atlas kuni tashkil etildi.",
         location="TIIU", date="2024-04-10 10:00"),
    dict(title="P. Qodirovning \"Yulduzli tunlar\" va Oybekning \"Navoiy\" — kitob tanlovi",
         description="Kitobxonlik tanlovida 2-kurs talabasi Islomov Mujahiddin 1-o'rinni egalladi.",
         location="TIIU", date="2024-03-20 14:00"),
    dict(title="\"Kitobxon\" tanlovi — Abdulla Qahhor asarlari",
         description="Adib Abdulla Qahhor asarlari bo'yicha tanlovda filologiya 2-kurs talabasi "
                     "Mamasoliyeva Marjona 1-o'rinni qo'lga kiritdi.",
         location="TIIU", date="2024-03-15 14:00"),
    dict(title="Sport musobaqasi — \"Talabalar ligasi\"",
         description="Voleybol, shashka va shaxmat bo'yicha \"Talabalar ligasi\" musobaqasi bo'lib o'tdi.",
         location="TIIU", date="2024-03-12 15:00"),
    dict(title="8-mart — Xalqaro xotin-qizlar kuni",
         description="Universitetda Xalqaro xotin-qizlar kuni tantanali nishonlandi.",
         location="TIIU", date="2024-03-08 12:00"),
]


def _dt(s):
    return timezone.make_aware(datetime.strptime(s, "%Y-%m-%d %H:%M"))


class Command(BaseCommand):
    help = "tiiu.uz ma'lumotlari bilan bazani to'ldiradi (settings, yo'nalish, rahbariyat, kafedra, markaz, o'qituvchi, yangilik, tadbir)"

    def handle(self, *args, **options):
        # ── SiteSettings ───────────────────────────────────────────────────
        s = SiteSettings.objects.first() or SiteSettings()
        for field, value in SETTINGS.items():
            setattr(s, field, value)
        s.save()
        self.stdout.write(self.style.SUCCESS("✓ SiteSettings yangilandi"))

        # ── Ta'lim yo'nalishlari ───────────────────────────────────────────
        for i, (name, desc) in enumerate(DIRECTIONS, start=1):
            Faculty.objects.update_or_create(
                name=name,
                defaults={"description": desc, "degree": "bachelor", "order": i},
            )
        self.stdout.write(self.style.SUCCESS(f"✓ Yo'nalishlar: jami {Faculty.objects.count()}"))

        # ── Rahbariyat ─────────────────────────────────────────────────────
        for d in LEADERSHIP:
            Leadership.objects.update_or_create(
                full_name=d["full_name"],
                defaults={**{k: v for k, v in d.items() if k != "full_name"}, "is_active": True},
            )
        self.stdout.write(self.style.SUCCESS(f"✓ Rahbariyat: jami {Leadership.objects.count()}"))

        # ── Kafedralar ─────────────────────────────────────────────────────
        for d in DEPARTMENTS:
            Department.objects.update_or_create(
                name=d["name"],
                defaults={"head": d["head"], "description": d["description"],
                          "order": d["order"], "is_active": True},
            )
        self.stdout.write(self.style.SUCCESS(f"✓ Kafedralar: jami {Department.objects.count()}"))

        # ── Markazlar ──────────────────────────────────────────────────────
        for d in CENTERS:
            Center.objects.update_or_create(
                name=d["name"],
                defaults={**{k: v for k, v in d.items() if k != "name"}, "is_active": True},
            )
        self.stdout.write(self.style.SUCCESS(f"✓ Markazlar: jami {Center.objects.count()}"))

        # ── O'qituvchilar (kafedraga bog'lanadi) ───────────────────────────
        dept_by_name = {d.name: d for d in Department.objects.all()}
        for d in TEACHERS:
            Teacher.objects.update_or_create(
                full_name=d["full_name"],
                defaults={"position": d["position"], "order": d["order"], "is_active": True,
                          "department": d["dept"], "kafedra": dept_by_name.get(d["dept"])},
            )
        self.stdout.write(self.style.SUCCESS(f"✓ O'qituvchilar: jami {Teacher.objects.count()}"))

        # ── Yangiliklar (kategoriya bilan) ─────────────────────────────────
        cat, _ = NewsCategory.objects.get_or_create(
            name="Universitet yangiliklari", defaults={"color": "#0b6b39"})
        for d in NEWS:
            News.objects.update_or_create(
                title=d["title"],
                defaults={"short_text": d["short_text"], "body": d["body"],
                          "category": cat, "author": "TIIU Matbuot xizmati",
                          "is_active": True, "is_featured": d.get("is_featured", False)},
            )
        self.stdout.write(self.style.SUCCESS(f"✓ Yangiliklar: jami {News.objects.count()}"))

        # ── Tadbirlar ──────────────────────────────────────────────────────
        for d in EVENTS:
            Event.objects.update_or_create(
                title=d["title"],
                defaults={"description": d["description"], "body": d["description"],
                          "location": d["location"], "event_date": _dt(d["date"]),
                          "is_active": True},
            )
        self.stdout.write(self.style.SUCCESS(f"✓ Tadbirlar: jami {Event.objects.count()}"))

        self.stdout.write(self.style.SUCCESS("\n✅ Barcha ma'lumotlar bazaga yozildi — /panel orqali tahrirlanadi."))
