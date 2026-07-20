"""tiiu.uz (WordPress) dan kontentni ko'chirish.

Ishlatish:
    python manage.py import_wp --since 2025-01-01
    python manage.py import_wp --dry-run

Buyruq idempotent: bir xil sarlavhali yangilik ikkinchi marta qo'shilmaydi,
shuning uchun uni xavfsiz qayta ishga tushirish mumkin.
"""
import json
import re
import unicodedata
import urllib.request
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from main.models import News, NewsCategory

API = "https://tiiu.uz/wp-json/wp/v2"
UA = {"User-Agent": "Mozilla/5.0 (tiiu-website content import)"}

# body shablonda {{ article.body|safe }} orqali xom HTML sifatida chiqadi,
# shuning uchun WordPress'dan kelgan hamma narsani saqlab bo'lmaydi: script,
# iframe va on* hodisa atributlari XSS yo'li ochadi. Faqat matn formatlash
# uchun kerakli teglar qoldiriladi.
ALLOWED_TAGS = {
    "p", "br", "strong", "b", "em", "i", "u", "ul", "ol", "li",
    "h2", "h3", "h4", "blockquote", "a", "img",
}
ALLOWED_ATTRS = {"a": {"href"}, "img": {"src", "alt"}}


class Sanitizer(HTMLParser):
    """WordPress HTML'ini xavfsiz teglar ro'yxatiga qisqartiradi."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "iframe", "form", "object", "embed"):
            self._skip_depth += 1
            return
        if self._skip_depth or tag not in ALLOWED_TAGS:
            return
        keep = ALLOWED_ATTRS.get(tag, set())
        kept = []
        for name, value in attrs:
            if name.lower() not in keep or not value:
                continue
            if name.lower() in ("href", "src") and value.strip().lower().startswith("javascript:"):
                continue
            kept.append(f' {name}="{value}"')
        self.out.append(f"<{tag}{''.join(kept)}>")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "iframe", "form", "object", "embed"):
            self._skip_depth = max(0, self._skip_depth - 1)
            return
        if self._skip_depth or tag not in ALLOWED_TAGS or tag in ("br", "img"):
            return
        self.out.append(f"</{tag}>")

    def handle_data(self, data):
        if not self._skip_depth:
            self.out.append(data)

    def result(self):
        html = "".join(self.out)
        html = re.sub(r"\[/?[a-z_]+[^\]]*\]", "", html)      # WP shortcode'lari
        html = re.sub(r"(\s*<p>\s*</p>\s*)+", "\n", html)     # bo'sh paragraflar
        return re.sub(r"\n{3,}", "\n\n", html).strip()


def sanitize(html):
    parser = Sanitizer()
    parser.feed(html)
    parser.close()
    return parser.result()


def plain(html):
    return " ".join(unescape(re.sub(r"<[^>]+>", " ", html)).split())


def norm_title(s):
    """Sarlavhalarni taqqoslash uchun normallashtirish (apostrof/registr farqi bo'ladi).

    Diakritik belgilar yo'qotiladi, lekin harflarning o'zi saqlanadi: ASCII'ga
    qisqartirish kirill sarlavhalarni butunlay bo'sh satrga aylantirib, barcha
    ruscha postlarni bitta kalitga yopishtirib qo'yadi.
    """
    s = plain(s).lower()
    for a, b in (("‘", "'"), ("’", "'"), ("ʻ", "'")):
        s = s.replace(a, b)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(re.sub(r"[^\w\s]", "", s, flags=re.UNICODE).split())[:60]


def localize_images(html, prefix):
    """body ichidagi tiiu.uz rasmlarini yuklab, src'ni mahalliy manzilga almashtiradi.

    WordPress rasmlarni http:// orqali beradi, sayt esa https'da ishlaydi —
    bunday rasmlarni brauzer mixed content sifatida bloklaydi va ular umuman
    ko'rinmaydi. Qolaversa, manba sayt o'zgarsa havolalar uziladi.
    """
    from django.conf import settings

    dest_dir = Path(settings.MEDIA_ROOT) / "news" / "inline"
    dest_dir.mkdir(parents=True, exist_ok=True)

    def repl(match):
        url = match.group(1)
        if "tiiu.uz" not in url:
            return match.group(0)
        name = f"{prefix}-{Path(url.split('?')[0]).name}"[:100]
        target = dest_dir / name
        if not target.exists():
            try:
                target.write_bytes(fetch_bytes(url.replace("http://", "https://")))
            except Exception:
                return match.group(0)  # yuklab bo'lmadi — asl havola qolsin
        return f'src="{settings.MEDIA_URL}news/inline/{name}"'

    return re.sub(r'src="([^"]+)"', repl, html)


def wp_datetime(post):
    """WP sanasini timezone'li datetime'ga aylantiradi.

    `date` mahalliy vaqt, timezone belgisisiz keladi; `date_gmt` esa UTC.
    USE_TZ=True bo'lgani uchun UTC variantini olib, unga tzinfo biriktiramiz.
    """
    raw = post.get("date_gmt") or post["date"]
    return datetime.fromisoformat(raw).replace(tzinfo=timezone.utc)


def fetch_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def fetch_bytes(url, timeout=60):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


class Command(BaseCommand):
    help = "tiiu.uz (WordPress) dan yangiliklarni ko'chiradi"

    def add_arguments(self, parser):
        parser.add_argument("--since", default="2025-01-01",
                            help="Shu sanadan keyingi postlar (YYYY-MM-DD)")
        parser.add_argument("--dry-run", action="store_true",
                            help="Hech narsa saqlanmaydi, faqat ko'rsatiladi")

    def handle(self, *args, **opts):
        since, dry = opts["since"], opts["dry_run"]
        self.stdout.write(f"tiiu.uz dan postlar olinmoqda (--since {since})...")

        posts = fetch_json(f"{API}/posts?per_page=100&page=1")
        existing = {norm_title(n.title) for n in News.objects.all()}

        todo = [p for p in posts
                if p["date"] >= since and norm_title(p["title"]["rendered"]) not in existing]
        todo.sort(key=lambda p: p["date"])
        self.stdout.write(f"Jami {len(posts)} post, ko'chiriladigan: {len(todo)}\n")

        category, _ = (NewsCategory.objects.get_or_create(
            name="Yangiliklar", defaults={"color": "#3b82f6"}) if not dry else (None, False))

        created = skipped = 0
        for p in todo:
            title = plain(p["title"]["rendered"])[:300]
            body = sanitize(p["content"]["rendered"])
            if not dry:
                body = localize_images(body, slugify(title)[:40] or "yangilik")
            excerpt = plain(p["excerpt"]["rendered"]) or plain(p["content"]["rendered"])

            image_url = self._featured_url(p)
            if not image_url:
                # News.image majburiy maydon — rasmsiz yozuvni saqlab bo'lmaydi.
                self.stdout.write(self.style.WARNING(f"  o'tkazildi (rasm yo'q): {title[:55]}"))
                skipped += 1
                continue

            self.stdout.write(f"  + {p['date'][:10]}  {title[:55]}")
            if dry:
                created += 1
                continue

            news = News(
                title=title,
                category=category,
                short_text=excerpt[:500],
                body=body,
                is_active=True,
            )
            ext = Path(image_url.split("?")[0]).suffix or ".jpg"
            news.image.save(f"{slugify(title)[:60] or 'yangilik'}{ext}",
                            ContentFile(fetch_bytes(image_url)), save=False)
            news.save()

            # created_at auto_now_add bo'lgani uchun konstruktorda o'rnatilmaydi —
            # WordPress'dagi haqiqiy sanani saqlash uchun keyin yangilanadi.
            # date_gmt ishlatiladi: `date` mahalliy va timezone'siz keladi, uni
            # to'g'ridan-to'g'ri yozish USE_TZ=True da sanani siljitib yuboradi.
            News.objects.filter(pk=news.pk).update(created_at=wp_datetime(p))
            created += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nTayyor. Qo'shildi: {created}, o'tkazildi: {skipped}"
            + (" (dry-run — hech narsa saqlanmadi)" if dry else "")))

    def _featured_url(self, post):
        media = (post.get("_embedded") or {}).get("wp:featuredmedia") or []
        if media and media[0].get("source_url"):
            return media[0]["source_url"]
        if post.get("featured_media"):
            try:
                return fetch_json(f"{API}/media/{post['featured_media']}").get("source_url")
            except Exception:
                return None
        return None
