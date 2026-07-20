"""
tiiu.uz (WordPress) REST API'dan yangiliklarni featured rasmlari bilan import qiladi.
Har yangilikning rasmi WordPress'dagi o'z featured-image'i — to'g'ri juftlanadi.
Ma'lumot DB'ga yoziladi (/panel'da tahrirlanadi); rasmlar media/news/ ga tushadi.
Idempotent: sarlavha bo'yicha update_or_create, rasm faqat yo'q bo'lsa yuklanadi.

    python manage.py import_tiiu_news --count 30
"""
import html
import re
import urllib.request

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from django.utils import timezone

from main.models import News, NewsCategory

API = "https://tiiu.uz/wp-json/wp/v2/posts?per_page={n}&page={p}&_embed=wp:featuredmedia"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}
TAGS = re.compile(r"<[^>]+>")
WS = re.compile(r"[ \t\r\f\v]*\n[ \t\r\f\v]*")
SPACES = re.compile(r"[ \t]{2,}")
MAX_BYTES = 8 * 1024 * 1024

# seed_tiiu bilan qo'lda kiritilgan taxminiy yangiliklar — real WP versiyasiga o'rin bo'shatadi
PLACEHOLDERS = [
    "Kelajagingizni biz bilan quring",
    "\"Buxgalteriya hisobi va audit\" yo'nalishi 1-kurs talabalari SHON-SHARAF muzeyiga ekskursiya uyushtirdi",
    "TIIU talabalari ishtirokida xavfsizlik kuni munosabati bilan profilaktik tadbir o'tkazildi",
    "Profilaktika inspektorlari tomonidan targ'ibot tadbirlari o'tkazildi",
]


def clean(s):
    s = html.unescape(TAGS.sub(" ", s or ""))
    s = s.replace("\xa0", " ").replace("​", "")
    s = WS.sub("\n", s)
    s = SPACES.sub(" ", s)
    return s.strip()


def _get_json(url):
    import json
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40))


def _get_bytes(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read()


class Command(BaseCommand):
    help = "tiiu.uz WordPress'dan yangiliklarni rasmlari bilan import qiladi"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=30, help="Nechta so'nggi yangilik")

    def handle(self, *args, **options):
        count = options["count"]
        cat, _ = NewsCategory.objects.get_or_create(
            name="Universitet yangiliklari", defaults={"color": "#0b6b39"})

        removed = News.objects.filter(title__in=PLACEHOLDERS).delete()[0]
        if removed:
            self.stdout.write(f"Taxminiy yangiliklar o'chirildi: {removed}")

        # sahifalab yig'amiz (WP max per_page=100)
        posts, page, per = [], 1, min(count, 100)
        while len(posts) < count:
            batch = _get_json(API.format(n=per, p=page))
            if not batch:
                break
            posts.extend(batch)
            if len(batch) < per:
                break
            page += 1
        posts = posts[:count]

        created = img_count = 0
        for p in posts:
            title = clean(p["title"]["rendered"])[:300]
            if not title:
                continue
            short = clean(p.get("excerpt", {}).get("rendered", ""))[:500]
            body = clean(p.get("content", {}).get("rendered", "")) or short
            if not short:
                short = (body[:300] or title)
            dt = parse_datetime(p["date"]) or timezone.now()
            if timezone.is_naive(dt):
                dt = timezone.make_aware(dt, timezone.get_current_timezone())

            obj, is_new = News.objects.update_or_create(
                title=title,
                defaults={"short_text": short, "body": body, "category": cat,
                          "author": "TIIU Matbuot xizmati", "is_active": True},
            )
            if is_new:
                created += 1
            # haqiqiy nashr sanasini o'rnatamiz (auto_now_add ni chetlab)
            News.objects.filter(pk=obj.pk).update(created_at=dt)

            # featured rasm (agar hali yo'q bo'lsa)
            if not obj.image:
                fm = (p.get("_embedded", {}).get("wp:featuredmedia") or [{}])[0]
                src = fm.get("source_url")
                if src:
                    data = self._img(src)
                    if data:
                        ext = ".png" if data[:8] == b"\x89PNG\r\n\x1a\n" else ".jpg"
                        obj.image.save(f"news-{obj.pk}{ext}", ContentFile(data), save=True)
                        img_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"\n✅ Yangiliklar: {created} yangi qo'shildi, {img_count} rasm yuklandi "
            f"(jami News: {News.objects.count()})"))

    def _img(self, url):
        try:
            data = _get_bytes(url)
        except Exception as e:
            self.stderr.write(f"  rasm yuklanmadi ({url[:60]}): {e}")
            return None
        if not (data[:3] == b"\xff\xd8\xff" or data[:8] == b"\x89PNG\r\n\x1a\n"):
            return None
        if len(data) > MAX_BYTES:
            return None
        return data
