"""
@tiiu_universiteti Telegram kanalidan olingan kontent bilan bazani to'ldiradi:
yangiliklar (e'lonlar) va bosh sahifa sliderlari.
Ma'lumot DB'ga yoziladi — /panel orqali tahrirlanadi. Rasmlar panelда qo'lda yuklanadi.
Idempotent (update_or_create) — qayta ishga tushirish xavfsiz.

    python manage.py seed_telegram
"""
from django.core.management.base import BaseCommand

from main.models import News, NewsCategory, Slider


# ── Yangiliklar / e'lonlar (t.me/tiiu_universiteti) ─────────────────────────
NEWS = [
    dict(title="Yoshlar kuni muborak!",
         short_text="Universitet jamoasi talabalarni Yoshlar kuni bilan tabriklaydi — yoshlik imkoniyatlar davri.",
         body="Toshkent ijtimoiy innovatsiya universiteti jamoasi barcha yoshlarni Yoshlar kuni bilan "
              "samimiy tabriklaydi. Yoshlik — imkoniyatlar davri: universitetimizga hujjat topshirib, "
              "kelajagingizni biz bilan boshlang."),
    dict(title="Barcha kunduzgi talabalar uchun oylik stipendiya",
         short_text="Kunduzgi ta'lim shaklidagi barcha talabalar oylik stipendiya olish imkoniyatiga ega.",
         body="Universitetda kunduzgi ta'lim shaklida tahsil olayotgan barcha talabalar oylik stipendiya "
              "bilan ta'minlanadi. Zamonaviy dasturlar, kuchli professor-o'qituvchilar tarkibi va "
              "innovatsion ta'lim muhiti sizni kutmoqda."),
    dict(title="Zamonaviy talabalar turar joyi",
         short_text="Viloyatlardan kelgan talabalar uchun qulay va xavfsiz zamonaviy turar joy sharoiti.",
         body="Universitet viloyatlardan kelgan talabalar uchun zamonaviy talabalar turar joyi bilan "
              "ta'minlaydi. Qulay va xavfsiz muhitda sifatli ta'lim oling — hujjatlaringizni o'z vaqtida "
              "topshiring."),
    dict(title="Arab tili yo'nalishi bitiruvchilari uchun kasb imkoniyatlari",
         short_text="O'qituvchilik, tarjimonlik, diplomatiya, turizm va xalqaro tashkilotlarda faoliyat.",
         body="Arab tili yo'nalishi bitiruvchilari uchun keng kasb imkoniyatlari ochiq: o'qituvchilik, "
              "tarjimonlik, diplomatiya sohasi, turizm hamda xalqaro tashkilotlarda faoliyat yuritish."),
    dict(title="TIIU talabasi xalqaro investitsiya forumida tarjimon bo'ldi",
         short_text="Talabamiz Toshkentdagi xalqaro forumda Ummon delegatsiyasiga tarjimonlik qildi.",
         body="Universitetimiz talabasi Toshkent shahrida bo'lib o'tgan xalqaro investitsiya forumida "
              "Ummon delegatsiyasi uchun tarjimon sifatida ishtirok etdi. Bu — talabalarimizning amaliy "
              "til ko'nikmalari va xalqaro tajribasining yorqin namunasi."),
    dict(title="Magistratura uchun chet tili sertifikati talab qilinmaydi",
         short_text="Magistratura qabuliga chet tili sertifikatini taqdim etish endi shart emas.",
         body="E'tiboringizga: magistratura bosqichiga qabul jarayonida chet tili sertifikatini taqdim "
              "etish talabi bekor qilindi. Bu qabul jarayonini abituriyentlar uchun yanada qulaylashtiradi."),
    dict(title="2026/2027 o'quv yili: 20 ga yaqin bakalavr va magistr dasturlari",
         short_text="Stipendiya va xalqaro almashinuv imkoniyatlari bilan 20 ga yaqin dastur.",
         body="2026/2027 o'quv yilida universitetda 20 ga yaqin bakalavr va magistr dasturlari mavjud. "
              "Talabalarga stipendiya, xalqaro almashinuv dasturlari va zamonaviy ta'lim sharoitlari taqdim etiladi."),
    dict(title="Hujjatlarni masofadan onlayn topshiring",
         short_text="qabul.tiiu.uz orqali hujjatlaringizni uydan turib onlayn topshirishingiz mumkin.",
         body="Universitetga hujjat topshirish endi yanada oson: qabul.tiiu.uz portali orqali "
              "hujjatlaringizni uydan turib masofadan onlayn topshirishingiz mumkin."),
]

# ── Bosh sahifa sliderlari (promo — rasmni panelда qo'shasiz) ───────────────
SLIDERS = [
    dict(title="Kelajakni biz bilan quring",
         subtitle="Toshkent ijtimoiy innovatsiya universitetiga 2026/2027 o'quv yili uchun hujjat topshiring.",
         btn_text="Hujjat topshirish", btn_url="https://qabul.tiiu.uz/", order=1),
    dict(title="Barcha kunduzgi talabalarga stipendiya",
         subtitle="Zamonaviy dasturlar, kuchli professor-o'qituvchilar va innovatsion ta'lim muhiti.",
         btn_text="Yo'nalishlar", btn_url="#faculties", order=2),
    dict(title="20 ga yaqin bakalavr va magistr dasturlari",
         subtitle="Stipendiya va xalqaro almashinuv imkoniyatlari bilan sifatli ta'lim.",
         btn_text="Batafsil", btn_url="#about", order=3),
]


class Command(BaseCommand):
    help = "@tiiu_universiteti Telegram kanalidan yangiliklar va sliderlarni bazaga yozadi"

    def handle(self, *args, **options):
        cat, _ = NewsCategory.objects.get_or_create(
            name="E'lonlar", defaults={"color": "#e4b363"})

        for d in NEWS:
            News.objects.update_or_create(
                title=d["title"],
                defaults={"short_text": d["short_text"], "body": d["body"],
                          "category": cat, "author": "TIIU Matbuot xizmati",
                          "is_active": True},
            )
        self.stdout.write(self.style.SUCCESS(f"✓ Telegram yangiliklari: jami {News.objects.count()}"))

        for d in SLIDERS:
            Slider.objects.update_or_create(
                title=d["title"],
                defaults={"subtitle": d["subtitle"], "btn_text": d["btn_text"],
                          "btn_url": d["btn_url"], "order": d["order"], "is_active": True},
            )
        self.stdout.write(self.style.SUCCESS(f"✓ Sliderlar: jami {Slider.objects.count()}"))
        self.stdout.write(self.style.SUCCESS(
            "\n✅ Telegram kontenti bazaga yozildi. Slayd rasmlarini /panel → Sliderlar bo'limида yuklang."))
