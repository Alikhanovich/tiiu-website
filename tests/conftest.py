"""
Umumiy fixture'lar va helper'lar — barcha testlar shulardan foydalanadi.
"""
import io
import json

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client

from main import models as m

User = get_user_model()


# ── Media izolyatsiyasi ───────────────────────────────────────────────────────
@pytest.fixture(autouse=True)
def _isolate_media(settings, tmp_path):
    """Har bir test yuklagan fayllarni vaqtinchalik papkaga yo'naltiradi —
    haqiqiy media/ papkasi ifloslanmasin."""
    settings.MEDIA_ROOT = str(tmp_path / "media")


# ── Rasm generatori ───────────────────────────────────────────────────────────
def make_image(name="test.png", w=1920, h=600, color=(120, 80, 200)):
    """Haqiqiy PNG bayt oqimi qaytaradi (ImageField validatsiyasidan o'tadi)."""
    from PIL import Image
    buf = io.BytesIO()
    Image.new("RGB", (w, h), color).save(buf, format="PNG")
    buf.seek(0)
    return SimpleUploadedFile(name, buf.read(), content_type="image/png")


@pytest.fixture
def image():
    return make_image()


@pytest.fixture
def small_file():
    """PDF/fayl maydonlari uchun oddiy fayl."""
    return SimpleUploadedFile("doc.pdf", b"%PDF-1.4 fake pdf bytes", content_type="application/pdf")


# ── Foydalanuvchilar ──────────────────────────────────────────────────────────
@pytest.fixture
def password():
    return "Str0ng-Pass-123!"


@pytest.fixture
def staff_user(db, password):
    return User.objects.create_user(
        username="admin", password=password, is_staff=True, is_active=True
    )


@pytest.fixture
def normal_user(db, password):
    """is_staff=False — panelga kira olmasligi kerak."""
    return User.objects.create_user(
        username="oddiy", password=password, is_staff=False, is_active=True
    )


# ── Clientlar ─────────────────────────────────────────────────────────────────
@pytest.fixture
def client():
    return Client()


@pytest.fixture
def staff_client(staff_user, password):
    c = Client()
    assert c.login(username=staff_user.username, password=password)
    return c


@pytest.fixture
def user_client(normal_user, password):
    c = Client()
    assert c.login(username=normal_user.username, password=password)
    return c


# ── JSON POST helper ──────────────────────────────────────────────────────────
class JsonHelper:
    """request.body = JSON bo'lgan endpointlar uchun (masalan api_login)."""
    def __init__(self, client):
        self.client = client

    def post(self, url, payload):
        return self.client.post(
            url, data=json.dumps(payload), content_type="application/json"
        )


@pytest.fixture
def jclient(client):
    return JsonHelper(client)


# ── Model fabrikalari (minimal, haqiqiy majburiy maydonlar bilan) ─────────────
@pytest.fixture
def faculty(db):
    return m.Faculty.objects.create(name="Iqtisodiyot yo'nalishi", description="Tavsif matni")


@pytest.fixture
def department(db, faculty):
    return m.Department.objects.create(name="Menejment kafedrasi", faculty=faculty)


@pytest.fixture
def news_category(db):
    return m.NewsCategory.objects.create(name="Universitet")


@pytest.fixture
def news(db, image, news_category):
    return m.News.objects.create(
        title="Yangi o'quv yili boshlandi",
        category=news_category,
        image=image,
        short_text="Qisqa matn",
        body="To'liq matn bu yerda.",
    )


@pytest.fixture
def event(db):
    from django.utils import timezone
    return m.Event.objects.create(
        title="Ochiq eshiklar kuni",
        event_date=timezone.now(),
        description="Tavsif",
    )


@pytest.fixture
def teacher(db, faculty):
    return m.Teacher.objects.create(full_name="Alisher Karimov", position="Dotsent", faculty=faculty)


@pytest.fixture
def gallery(db):
    return m.Gallery.objects.create(title="Bitiruv marosimi 2025")


@pytest.fixture
def department_page(db, department):
    return department


@pytest.fixture
def center(db):
    return m.Center.objects.create(name="Xalqaro aloqalar markazi")


@pytest.fixture
def static_page(db):
    return m.StaticPage.objects.create(title="Maxfiylik siyosati", slug="maxfiylik", body="<p>Matn</p>")


@pytest.fixture
def leadership(db):
    return m.Leadership.objects.create(full_name="Rektor Ismi", position="Rektor")
