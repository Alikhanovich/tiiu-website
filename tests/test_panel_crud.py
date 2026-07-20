"""
Panel CRUD testlari — resurslar bo'yicha:
  - POST (create) yangi obyekt yaratadi
  - GET (list) sahifalangan ro'yxat qaytaradi
  - POST detail (update) mavjud obyektni yangilaydi
  - DELETE o'chiradi
  - yo'q pk 404 (IDOR himoyasi — mavjud bo'lmagan resurs)
Barcha so'rovlar staff_client orqali (auth allaqachon test_panel_auth'da tekshirilgan).
"""
import pytest

from main import models as m

pytestmark = pytest.mark.django_db


# ── Faculty (to'liq CRUD sikli) ───────────────────────────────────────────────
class TestFacultyCRUD:
    LIST = "/panel/api/faculty/"

    def test_create(self, staff_client):
        resp = staff_client.post(self.LIST, {
            "name": "Yangi yo'nalish", "description": "Tavsif",
            "degree": "master", "duration": "2", "order": "1", "is_active": "true",
        })
        assert resp.status_code == 200
        body = resp.json()
        assert body["success"] is True
        assert m.Faculty.objects.filter(name="Yangi yo'nalish").exists()
        f = m.Faculty.objects.get(name="Yangi yo'nalish")
        assert f.degree == "master"
        assert f.duration == 2
        assert f.is_active is True

    def test_list_pagination(self, staff_client):
        for i in range(25):
            m.Faculty.objects.create(name=f"F{i}", description="d")
        resp = staff_client.get(self.LIST)
        body = resp.json()
        assert body["success"] is True
        assert body["total"] == 25
        assert len(body["data"]) == 20  # per=20
        assert body["pages"] == 2

    def test_update(self, staff_client, faculty):
        resp = staff_client.post(f"{self.LIST}{faculty.pk}/", {"name": "Yangilangan nom"})
        assert resp.status_code == 200
        faculty.refresh_from_db()
        assert faculty.name == "Yangilangan nom"

    def test_update_is_active_toggle(self, staff_client, faculty):
        staff_client.post(f"{self.LIST}{faculty.pk}/", {"is_active": "false"})
        faculty.refresh_from_db()
        assert faculty.is_active is False

    def test_delete(self, staff_client, faculty):
        resp = staff_client.delete(f"{self.LIST}{faculty.pk}/")
        assert resp.status_code == 200
        assert not m.Faculty.objects.filter(pk=faculty.pk).exists()

    def test_detail_missing_pk_404(self, staff_client):
        resp = staff_client.get(f"{self.LIST}999999/")
        assert resp.status_code == 404

    def test_delete_missing_pk_404(self, staff_client):
        resp = staff_client.delete(f"{self.LIST}999999/")
        assert resp.status_code == 404


# ── News (kategoriyali + rasmli) ──────────────────────────────────────────────
class TestNewsCRUD:
    LIST = "/panel/api/news/"

    def test_create_with_image(self, staff_client, image, news_category):
        resp = staff_client.post(self.LIST, {
            "title": "Panel orqali xabar",
            "category": str(news_category.pk),
            "short_text": "qisqa", "body": "to'liq",
            "is_active": "true", "image": image,
        })
        assert resp.status_code == 200
        assert m.News.objects.filter(title="Panel orqali xabar").exists()

    def test_list(self, staff_client, news):
        resp = staff_client.get(self.LIST)
        assert resp.status_code == 200
        assert resp.json()["total"] >= 1

    def test_delete(self, staff_client, news):
        resp = staff_client.delete(f"{self.LIST}{news.pk}/")
        assert resp.status_code == 200
        assert not m.News.objects.filter(pk=news.pk).exists()

    def test_missing_404(self, staff_client):
        assert staff_client.get(f"{self.LIST}999999/").status_code == 404


# ── Teacher ───────────────────────────────────────────────────────────────────
class TestTeacherCRUD:
    LIST = "/panel/api/teachers/"

    def test_create(self, staff_client):
        resp = staff_client.post(self.LIST, {
            "full_name": "Yangi O'qituvchi", "position": "Assistent",
            "experience": "3", "order": "0", "is_active": "true",
        })
        assert resp.status_code == 200
        assert m.Teacher.objects.filter(full_name="Yangi O'qituvchi").exists()

    def test_update(self, staff_client, teacher):
        staff_client.post(f"{self.LIST}{teacher.pk}/", {"position": "Katta o'qituvchi"})
        teacher.refresh_from_db()
        assert teacher.position == "Katta o'qituvchi"

    def test_delete_and_404(self, staff_client, teacher):
        assert staff_client.delete(f"{self.LIST}{teacher.pk}/").status_code == 200
        assert staff_client.get(f"{self.LIST}{teacher.pk}/").status_code == 404


# ── Event ─────────────────────────────────────────────────────────────────────
class TestEventCRUD:
    LIST = "/panel/api/events/"

    def test_create(self, staff_client):
        resp = staff_client.post(self.LIST, {
            "title": "Yangi tadbir",
            "event_date": "2026-09-01T10:00",
            "description": "Tavsif", "is_active": "true",
        })
        assert resp.status_code == 200
        assert m.Event.objects.filter(title="Yangi tadbir").exists()

    def test_list(self, staff_client, event):
        assert staff_client.get(self.LIST).json()["total"] >= 1

    def test_delete(self, staff_client, event):
        assert staff_client.delete(f"{self.LIST}{event.pk}/").status_code == 200


# ── Leadership ────────────────────────────────────────────────────────────────
class TestLeadershipCRUD:
    LIST = "/panel/api/leadership/"

    def test_create(self, staff_client):
        resp = staff_client.post(self.LIST, {
            "full_name": "Prorektor Ismi", "position": "Prorektor",
            "order": "1", "is_active": "true",
        })
        assert resp.status_code == 200
        assert m.Leadership.objects.filter(full_name="Prorektor Ismi").exists()

    def test_delete_404(self, staff_client):
        assert staff_client.delete(f"{self.LIST}999999/").status_code == 404


# ── Department ────────────────────────────────────────────────────────────────
class TestDepartmentCRUD:
    LIST = "/panel/api/departments/"

    def test_create(self, staff_client, faculty):
        resp = staff_client.post(self.LIST, {
            "name": "Yangi kafedra", "faculty": str(faculty.pk),
            "order": "0", "is_active": "true",
        })
        assert resp.status_code == 200
        assert m.Department.objects.filter(name="Yangi kafedra").exists()


# ── Center ────────────────────────────────────────────────────────────────────
class TestCenterCRUD:
    LIST = "/panel/api/centers/"

    def test_create(self, staff_client):
        resp = staff_client.post(self.LIST, {
            "name": "Yangi markaz", "order": "0", "is_active": "true",
        })
        assert resp.status_code == 200
        assert m.Center.objects.filter(name="Yangi markaz").exists()


# ── Messages (o'qish + status + o'chirish) ────────────────────────────────────
class TestMessages:
    LIST = "/panel/api/messages/"

    @pytest.fixture
    def message(self, db):
        return m.ContactMessage.objects.create(
            first_name="Ali", last_name="Vali", message="Test xabar",
        )

    def test_list(self, staff_client, message):
        resp = staff_client.get(self.LIST)
        assert resp.status_code == 200
        assert resp.json()["total"] >= 1

    def test_delete(self, staff_client, message):
        resp = staff_client.delete(f"{self.LIST}{message.pk}/")
        assert resp.status_code == 200
        assert not m.ContactMessage.objects.filter(pk=message.pk).exists()

    def test_missing_404(self, staff_client):
        assert staff_client.get(f"{self.LIST}999999/").status_code == 404


# ── Static Pages ──────────────────────────────────────────────────────────────
class TestPagesCRUD:
    LIST = "/panel/api/pages/"

    def test_create(self, staff_client):
        resp = staff_client.post(self.LIST, {
            "title": "Yangi sahifa", "slug": "yangi-sahifa",
            "body": "<p>Matn</p>", "is_active": "true",
        })
        assert resp.status_code == 200
        assert m.StaticPage.objects.filter(slug="yangi-sahifa").exists()


# ── Ilm-fan resurslari (create + 404) ─────────────────────────────────────────
class TestScienceResources:
    def test_article_create(self, staff_client):
        resp = staff_client.post("/panel/api/articles/", {
            "title": "Ilmiy maqola", "authors": "Karimov A.",
            "language": "uz", "is_active": "true",
        })
        assert resp.status_code == 200
        assert m.ScientificArticle.objects.filter(title="Ilmiy maqola").exists()

    def test_dissertation_create(self, staff_client):
        resp = staff_client.post("/panel/api/dissertations/", {
            "title": "Dissertatsiya", "author": "Aliyev B.",
            "degree": "phd", "is_active": "true",
        })
        assert resp.status_code == 200
        assert m.Dissertation.objects.filter(title="Dissertatsiya").exists()

    def test_conference_create(self, staff_client):
        resp = staff_client.post("/panel/api/conferences/", {
            "title": "Konferensiya", "start_date": "2026-10-01T09:00",
            "is_active": "true",
        })
        assert resp.status_code == 200
        assert m.Conference.objects.filter(title="Konferensiya").exists()

    def test_conference_create_date_only(self, staff_client):
        """Sana-only formatida ishlaydimi (parse_date qabul qiladigan format)."""
        resp = staff_client.post("/panel/api/conferences/", {
            "title": "Konf sana", "start_date": "2026-10-01",
            "is_active": "true",
        })
        assert resp.status_code == 200
        assert m.Conference.objects.filter(title="Konf sana").exists()

    def test_journal_create(self, staff_client):
        resp = staff_client.post("/panel/api/journals/", {
            "title": "Jurnal soni", "year": "2026", "issue_number": "1",
            "is_active": "true",
        })
        assert resp.status_code == 200
        assert m.JournalIssue.objects.filter(year=2026, issue_number=1).exists()


# ── Talabalarga bo'lim resurslari ─────────────────────────────────────────────
class TestStudentResources:
    def test_video_create(self, staff_client):
        resp = staff_client.post("/panel/api/videos/", {
            "title": "Video dars", "youtube_url": "https://youtube.com/watch?v=x",
            "is_active": "true",
        })
        assert resp.status_code == 200
        assert m.VideoLesson.objects.filter(title="Video dars").exists()

    def test_talented_create(self, staff_client):
        resp = staff_client.post("/panel/api/talented/", {
            "full_name": "Iqtidorli Talaba", "achievement": "1-o'rin",
            "year": "2026", "is_active": "true",
        })
        assert resp.status_code == 200
        assert m.TalentedStudent.objects.filter(full_name="Iqtidorli Talaba").exists()

    def test_contest_create(self, staff_client):
        resp = staff_client.post("/panel/api/contests/", {
            "title": "Tanlov", "is_active": "true",
        })
        assert resp.status_code == 200
        assert m.Contest.objects.filter(title="Tanlov").exists()
