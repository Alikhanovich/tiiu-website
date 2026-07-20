"""
Panel autentifikatsiya va ruxsat (xavfsizlik) testlari:
  - login: to'g'ri / noto'g'ri parol / staff bo'lmagan user
  - logout, me
  - @staff_only himoyasi: anonim va oddiy user 403 oladi
  - staff bo'lmagan user login qila olmaydi (401)
"""
import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


# ── Login ─────────────────────────────────────────────────────────────────────
class TestLogin:
    URL = "/panel/api/login/"

    def test_valid_staff_login(self, jclient, staff_user, password):
        resp = jclient.post(self.URL, {"username": staff_user.username, "password": password})
        assert resp.status_code == 200
        body = resp.json()
        assert body["success"] is True
        assert body["username"] == staff_user.username

    def test_wrong_password(self, jclient, staff_user):
        resp = jclient.post(self.URL, {"username": staff_user.username, "password": "notri"})
        assert resp.status_code == 401
        assert resp.json()["success"] is False

    def test_nonexistent_user(self, jclient):
        resp = jclient.post(self.URL, {"username": "yoq", "password": "x"})
        assert resp.status_code == 401

    def test_non_staff_cannot_login(self, jclient, normal_user, password):
        """is_staff=False bo'lgan user to'g'ri parol bilan ham panelga kira olmaydi."""
        resp = jclient.post(self.URL, {"username": normal_user.username, "password": password})
        assert resp.status_code == 401
        assert resp.json()["success"] is False

    def test_login_only_post(self, client):
        resp = client.get(self.URL)
        assert resp.status_code == 405  # require_http_methods(['POST'])


# ── me / logout ───────────────────────────────────────────────────────────────
class TestMeLogout:
    def test_me_anonymous(self, client):
        resp = client.get("/panel/api/me/")
        assert resp.status_code == 200
        assert resp.json()["auth"] is False

    def test_me_authenticated(self, staff_client):
        resp = staff_client.get("/panel/api/me/")
        assert resp.json()["auth"] is True

    def test_logout(self, staff_client):
        resp = staff_client.post("/panel/api/logout/")
        assert resp.status_code == 200
        assert resp.json()["success"] is True
        # logout'dan keyin me anonim bo'lishi kerak
        assert staff_client.get("/panel/api/me/").json()["auth"] is False


# ── @staff_only himoyasi ──────────────────────────────────────────────────────
# Har bir himoyalangan GET endpoint anonim va oddiy user uchun 403 qaytarishi kerak.
PROTECTED_GET_ENDPOINTS = [
    "/panel/api/stats/",
    "/panel/api/settings/",
    "/panel/api/sliders/",
    "/panel/api/faculty/",
    "/panel/api/teachers/",
    "/panel/api/news/",
    "/panel/api/leadership/",
    "/panel/api/departments/",
    "/panel/api/centers/",
    "/panel/api/events/",
    "/panel/api/faqs/",
    "/panel/api/partners/",
    "/panel/api/messages/",
    "/panel/api/pages/",
    "/panel/api/articles/",
    "/panel/api/dissertations/",
    "/panel/api/conferences/",
    "/panel/api/contests/",
    "/panel/api/videos/",
    "/panel/api/talented/",
    "/panel/api/journals/",
    "/panel/api/schedules/",
    "/panel/api/library/",
]


@pytest.mark.parametrize("url", PROTECTED_GET_ENDPOINTS)
def test_anonymous_gets_403(client, url):
    resp = client.get(url)
    assert resp.status_code == 403, f"{url} anonim uchun {resp.status_code}"


@pytest.mark.parametrize("url", PROTECTED_GET_ENDPOINTS)
def test_non_staff_gets_403(user_client, url):
    resp = user_client.get(url)
    assert resp.status_code == 403, f"{url} oddiy user uchun {resp.status_code}"


@pytest.mark.parametrize("url", PROTECTED_GET_ENDPOINTS)
def test_staff_gets_200(staff_client, url):
    resp = staff_client.get(url)
    assert resp.status_code == 200, f"{url} staff uchun {resp.status_code}"


# ── Panel SPA shell ───────────────────────────────────────────────────────────
def test_panel_home_renders(client):
    resp = client.get("/panel/")
    assert resp.status_code == 200
    # CSRF cookie o'rnatilishi kerak (@ensure_csrf_cookie)
    assert "csrftoken" in resp.cookies
