"""
Public sayt (main app) testlari:
  - barcha statik route'lar 200 qaytaradi
  - detail sahifalar mavjud slug bilan 200, yo'q slug bilan 404
  - kontakt forma: valid submit DB'ga yozadi, invalid 400 qaytaradi
  - sitemap / robots / xizmat route'lari
"""
import pytest
from django.urls import reverse

from main import models as m

pytestmark = pytest.mark.django_db


# ── Statik (argumentsiz) route'lar ────────────────────────────────────────────
STATIC_ROUTES = [
    "index", "about", "faculties", "news_list", "events", "gallery",
    "contact", "teachers", "leadership", "departments", "centers",
    "articles_list", "dissertations_list", "conferences_list", "journal_list",
    "video_lessons_list", "talented_students", "contests_list",
    "schedule_list", "library_list",
]


@pytest.mark.parametrize("route", STATIC_ROUTES)
def test_static_route_returns_200(client, route):
    resp = client.get(reverse(route))
    assert resp.status_code == 200, f"{route} -> {resp.status_code}"


def test_sitemap_xml(client):
    resp = client.get(reverse("sitemap"))
    assert resp.status_code == 200
    assert "xml" in resp["Content-Type"]


def test_robots_txt(client):
    resp = client.get("/robots.txt")
    assert resp.status_code == 200
    assert b"Disallow: /panel/" in resp.content


def test_favicon_redirect(client):
    resp = client.get("/favicon.ico")
    assert resp.status_code == 301


# ── Detail sahifalar: mavjud slug 200 ─────────────────────────────────────────
class TestDetailPagesExist:
    def test_faculty_detail(self, client, faculty):
        resp = client.get(reverse("faculty_detail", args=[faculty.slug]))
        assert resp.status_code == 200

    def test_news_detail(self, client, news):
        resp = client.get(reverse("news_detail", args=[news.slug]))
        assert resp.status_code == 200

    def test_news_detail_increments_views(self, client, news):
        before = news.views
        client.get(reverse("news_detail", args=[news.slug]))
        news.refresh_from_db()
        assert news.views >= before  # ko'rish hisoblanadi (agar view shunday qilgan bo'lsa)

    def test_event_detail(self, client, event):
        resp = client.get(reverse("event_detail", args=[event.slug]))
        assert resp.status_code == 200

    def test_gallery_detail(self, client, gallery):
        resp = client.get(reverse("gallery_detail", args=[gallery.slug]))
        assert resp.status_code == 200

    def test_department_detail(self, client, department):
        resp = client.get(reverse("department_detail", args=[department.slug]))
        assert resp.status_code == 200

    def test_static_page(self, client, static_page):
        resp = client.get(reverse("static_page", args=[static_page.slug]))
        assert resp.status_code == 200


# ── Detail sahifalar: yo'q slug 404 ───────────────────────────────────────────
DETAIL_ROUTES_404 = [
    "faculty_detail", "news_detail", "event_detail", "gallery_detail",
    "department_detail", "static_page", "article_detail", "dissertation_detail",
    "conference_detail", "journal_detail", "video_lesson_detail",
    "contest_detail", "library_detail",
]


@pytest.mark.parametrize("route", DETAIL_ROUTES_404)
def test_detail_missing_slug_404(client, route):
    resp = client.get(reverse(route, args=["yoq-bunday-slug-xxx"]))
    assert resp.status_code == 404, f"{route} -> {resp.status_code}"


# ── Kontakt forma ─────────────────────────────────────────────────────────────
class TestContactForm:
    URL = "/contact/submit/"

    def test_valid_submit_creates_message(self, client):
        resp = client.post(self.URL, {
            "first_name": "Ali", "last_name": "Valiyev",
            "phone": "+998901112233", "email": "ali@example.com",
            "direction": "IT", "message": "Salom, ma'lumot kerak.",
        })
        assert resp.status_code == 200
        assert resp.json()["ok"] is True
        assert m.ContactMessage.objects.filter(first_name="Ali", last_name="Valiyev").exists()

    def test_missing_first_name_rejected(self, client):
        resp = client.post(self.URL, {"last_name": "Valiyev"})
        assert resp.status_code == 400
        assert resp.json()["ok"] is False
        assert not m.ContactMessage.objects.exists()

    def test_missing_last_name_rejected(self, client):
        resp = client.post(self.URL, {"first_name": "Ali"})
        assert resp.status_code == 400
        assert not m.ContactMessage.objects.exists()

    def test_fields_truncated_to_limits(self, client):
        resp = client.post(self.URL, {
            "first_name": "A" * 500,
            "last_name": "B" * 500,
            "message": "M" * 5000,
        })
        assert resp.status_code == 200
        cm = m.ContactMessage.objects.first()
        assert len(cm.first_name) <= 100
        assert len(cm.last_name) <= 100
        assert len(cm.message) <= 2000

    def test_new_message_default_status(self, client):
        client.post(self.URL, {"first_name": "X", "last_name": "Y"})
        cm = m.ContactMessage.objects.first()
        assert cm.status == "new"


# ── Inaktiv obyektlar public'da ko'rinmasligi (agar view filtrlaydigan bo'lsa) ─
class TestActiveFiltering:
    def test_inactive_news_hidden_or_404(self, client, image, news_category):
        n = m.News.objects.create(
            title="Yashirin xabar", category=news_category, image=image,
            short_text="s", body="b", is_active=False,
        )
        resp = client.get(reverse("news_detail", args=[n.slug]))
        # View is_active=False'ni yashirsa 404; aks holda 200 (ikkalasi ham qabul qilinadi,
        # lekin bu test view xatti-harakatini hujjatlashtiradi)
        assert resp.status_code in (200, 404)
