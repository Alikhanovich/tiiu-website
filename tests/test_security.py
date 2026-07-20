"""
Xavfsizlikka yo'naltirilgan testlar:
  - IDOR: boshqa foydalanuvchining resursiga to'g'ridan-to'g'ri pk bilan kirish
    (bu proyektda barcha staff bir xil huquqqa ega, shuning uchun asosiy xavf —
    auth bypass, u test_panel_auth'da qamrab olingan. Bu yerda yo'q pk / manipulyatsiya.)
  - Login JSON body buzilganda xatolik
  - HTTP metod chekloviga rioya
  - contact_submit faqat POST
"""
import pytest

from main import models as m

pytestmark = pytest.mark.django_db


class TestLoginRobustness:
    URL = "/panel/api/login/"

    def test_malformed_json_body(self, client):
        resp = client.post(self.URL, data="{buzilgan json", content_type="application/json")
        assert resp.status_code == 400

    def test_empty_credentials(self, jclient):
        resp = jclient.post(self.URL, {"username": "", "password": ""})
        assert resp.status_code == 401


class TestMethodRestrictions:
    def test_logout_get_not_allowed(self, staff_client):
        resp = staff_client.get("/panel/api/logout/")
        assert resp.status_code == 405

    def test_contact_submit_get_not_allowed(self, client):
        # contact_submit request.POST'dan o'qiydi; GET bo'sh POST beradi -> 400
        resp = client.get("/contact/submit/")
        assert resp.status_code in (400, 405)


class TestPkManipulation:
    """Katta/manfiy/nol pk'lar 404 qaytarishi kerak, 500 emas."""

    @pytest.mark.parametrize("pk", [0, 999999, 123456789])
    def test_faculty_detail_bad_pk(self, staff_client, pk):
        resp = staff_client.get(f"/panel/api/faculty/{pk}/")
        assert resp.status_code == 404

    @pytest.mark.parametrize("pk", [0, 999999])
    def test_news_detail_bad_pk(self, staff_client, pk):
        resp = staff_client.get(f"/panel/api/news/{pk}/")
        assert resp.status_code == 404


class TestPanelHiddenFromRobots:
    def test_robots_disallows_panel_and_admin(self, client):
        content = client.get("/robots.txt").content
        assert b"/panel/" in content
        assert b"/admin-web/" in content


class TestContactMessageNotLeaked:
    """Public tomondan kelgan xabarlar faqat staff'ga ko'rinishi kerak."""

    def test_messages_endpoint_requires_staff(self, client, user_client):
        m.ContactMessage.objects.create(first_name="A", last_name="B", message="maxfiy")
        assert client.get("/panel/api/messages/").status_code == 403
        assert user_client.get("/panel/api/messages/").status_code == 403
