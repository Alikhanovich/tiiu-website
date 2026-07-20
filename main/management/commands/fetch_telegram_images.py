"""
@tiiu_universiteti Telegram kanalidan rasmlarni yuklab, bosh sahifa sliderlariga
biriktiradi. Faqat rasm (JPEG/PNG) fayllari qabul qilinadi, hajm cheklangan.
Rasmlar media/sliders/ ga tushadi va /panel orqali almashtirilishi mumkin.

    python manage.py fetch_telegram_images
"""
import re
import urllib.request

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from main.models import Slider, News

CHANNEL = "https://t.me/s/tiiu_universiteti"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}
MAX_BYTES = 8 * 1024 * 1024


def _get(url, timeout=30):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()


class Command(BaseCommand):
    help = "Telegram kanalidan rasm yuklab sliderlarga biriktiradi"

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true",
                            help="Rasmi bor sliderlarni ham qayta yozadi")

    def handle(self, *args, **options):
        html = _get(CHANNEL).decode("utf-8", "ignore")
        urls, seen = [], set()
        for u in re.findall(r"background-image:url\('(https://[^']+)'\)", html):
            if u not in seen:
                seen.add(u)
                urls.append(u)
        self.stdout.write(f"Kanaldan topilgan rasmlar: {len(urls)}")

        sliders = list(Slider.objects.order_by("order"))
        for i, sl in enumerate(sliders):
            if sl.image and not options["force"]:
                self.stdout.write(f"— {sl.title[:40]}: rasmi bor, o'tkazib yuborildi")
                continue
            if i >= len(urls):
                break
            data = self._download(urls[i])
            if not data:
                continue
            sl.image.save(f"slider-{sl.pk}.jpg", ContentFile(data), save=True)
            self.stdout.write(self.style.SUCCESS(
                f"✓ {sl.title[:40]} ← rasm ({len(data) // 1024} KB)"))

        # ── E'lonlar (Telegram'dan kelgan yangiliklar) uchun rasm ──────────
        # kanaldagi keyingi (sliderlardan keyingi) rasmlarni biriktiramiz
        idx = len(sliders)
        elonlar = News.objects.filter(category__name="E'lonlar").order_by("pk")
        for news in elonlar:
            if news.image and not options["force"]:
                continue
            while idx < len(urls):
                data = self._download(urls[idx])
                idx += 1
                if data:
                    news.image.save(f"news-{news.pk}.jpg", ContentFile(data), save=True)
                    self.stdout.write(self.style.SUCCESS(
                        f"✓ [e'lon] {news.title[:38]} ← rasm ({len(data) // 1024} KB)"))
                    break

        self.stdout.write(self.style.SUCCESS("\n✅ Telegram rasmlari yuklandi (slider + e'lonlar)."))

    def _download(self, url):
        try:
            data = _get(url)
        except Exception as e:
            self.stderr.write(f"  yuklab bo'lmadi: {e}")
            return None
        if not (data[:3] == b"\xff\xd8\xff" or data[:8] == b"\x89PNG\r\n\x1a\n"):
            self.stderr.write("  rasm (JPEG/PNG) emas, o'tkazib yuborildi")
            return None
        if len(data) > MAX_BYTES:
            self.stderr.write("  fayl juda katta, o'tkazib yuborildi")
            return None
        return data
