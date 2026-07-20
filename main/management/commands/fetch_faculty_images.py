"""
Har bir ta'lim yo'nalishiga mavzuga mos real (Creative Commons) rasm yuklaydi.
Manba: loremflickr.com (kalit so'z bo'yicha real Flickr CC fotolari).
Rasmlar media/faculties/ ga tushadi va /panel orqali almashtiriladi.
Idempotent: rasmi bor yo'nalish o'tkazib yuboriladi (--force bilan qayta yoziladi).

    python manage.py fetch_faculty_images
"""
import urllib.request

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from main.models import Faculty

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}

# Yo'nalish nomi -> loremflickr kalit so'zi (mavzuga mos)
KEYWORDS = {
    "Iqtisodiyot": "economics",
    "Moliya va moliyaviy texnologiyalar": "finance",
    "Buxgalteriya hisobi va audit": "accounting",
    "Bank ishi": "bank",
    "Axborot tizimlari va texnologiyalari": "technology",
    "Psixologiya": "psychology",
    "Boshlang'ich ta'lim": "classroom",
    "Maktabgacha ta'lim": "kindergarten",
    "Jismoniy madaniyat": "sport",
    "Filologiya va tillarni o'qitish": "books",
}
DEFAULT_KW = "university"


def _download(keyword):
    url = f"https://loremflickr.com/1200/600/{keyword}"
    data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read()
    if not (data[:3] == b"\xff\xd8\xff" or data[:8] == b"\x89PNG\r\n\x1a\n"):
        return None
    return data


class Command(BaseCommand):
    help = "Yo'nalishlarga mavzuga mos real rasm yuklaydi (loremflickr)"

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Rasmi bor yo'nalishni ham qayta yozadi")

    def handle(self, *args, **options):
        n = 0
        for f in Faculty.objects.all():
            if f.image and not options["force"]:
                self.stdout.write(f"— {f.name[:35]}: rasmi bor, o'tkazildi")
                continue
            kw = KEYWORDS.get(f.name, DEFAULT_KW)
            try:
                data = _download(kw)
            except Exception as e:
                self.stderr.write(f"  {f.name[:35]}: xato ({kw}) — {e}")
                continue
            if not data:
                continue
            f.image.save(f"faculty-{f.pk}.jpg", ContentFile(data), save=True)
            n += 1
            self.stdout.write(self.style.SUCCESS(f"✓ {f.name[:35]} ← {kw} ({len(data)//1024} KB)"))
        self.stdout.write(self.style.SUCCESS(f"\n✅ Yo'nalish rasmlari: {n} ta yuklandi."))
