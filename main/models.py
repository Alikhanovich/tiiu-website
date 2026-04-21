from django.db import models
from django.utils.text import slugify


# ─── Site Settings ───────────────────────────────────────────────────────────
class SiteSettings(models.Model):
    site_name       = models.CharField("Sayt nomi", max_length=200, default="TIIU")
    site_name_full  = models.CharField("To'liq nom", max_length=300,
                                       default="Toshkent ijtimoiy innovatsiya universiteti")
    logo            = models.ImageField("Logo", upload_to="settings/", blank=True, null=True)
    favicon         = models.ImageField("Favicon", upload_to="settings/", blank=True, null=True)
    address         = models.TextField("Manzil",
                                       default="Toshkent, Sergeli tumani, Uzumzor ko'chasi, 37")
    phone1          = models.CharField("Telefon 1", max_length=30, default="+998 78 113 17 17")
    phone2          = models.CharField("Telefon 2", max_length=30, blank=True)
    email           = models.EmailField("Email", default="info@tiiu.uz")
    work_hours      = models.CharField("Ish vaqti", max_length=200,
                                       default="Du–Ju: 9:00–18:00 | Shanba: 9:00–14:00")
    facebook        = models.URLField("Facebook", blank=True)
    instagram       = models.URLField("Instagram", blank=True)
    telegram        = models.URLField("Telegram", blank=True)
    youtube         = models.URLField("YouTube", blank=True)
    founded_year    = models.PositiveIntegerField("Tashkil yili", default=2015)
    student_count   = models.PositiveIntegerField("Talabalar soni", default=1200)
    teacher_count   = models.PositiveIntegerField("O'qituvchilar soni", default=50)
    direction_count = models.PositiveIntegerField("Yo'nalishlar soni", default=9)
    about_text      = models.TextField("Universitet haqida (qisqa)", blank=True)
    hero_title      = models.CharField("Hero sarlavha", max_length=200,
                                       default="Kelajakni bugun shakllantir")
    hero_subtitle   = models.TextField("Hero izoh", blank=True,
                                       default="Toshkent ijtimoiy innovatsiya universiteti — "
                                               "ilg'or ta'lim texnologiyalari asosida zamonaviy "
                                               "mutaxassislar tayyorlaydigan nodavlat oliy ta'lim muassasasi.")

    class Meta:
        verbose_name = "Sayt sozlamalari"
        verbose_name_plural = "Sayt sozlamalari"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


# ─── Slider ──────────────────────────────────────────────────────────────────
class Slider(models.Model):
    title     = models.CharField("Sarlavha", max_length=200)
    subtitle  = models.TextField("Izoh", blank=True)
    image     = models.ImageField("Rasm", upload_to="sliders/")
    btn_text  = models.CharField("Tugma matni", max_length=100, blank=True)
    btn_url   = models.CharField("Tugma URL", max_length=200, blank=True, default="/")
    order     = models.PositiveIntegerField("Tartib", default=0)
    is_active = models.BooleanField("Faol", default=True)

    class Meta:
        verbose_name = "Slider"
        verbose_name_plural = "Sliderlar"
        ordering = ["order"]

    def __str__(self):
        return self.title


# ─── Faculty ─────────────────────────────────────────────────────────────────
class Faculty(models.Model):
    DEGREE_CHOICES = [("bachelor", "Bakalavr"), ("master", "Magistr")]

    name        = models.CharField("Nomi", max_length=300)
    slug        = models.SlugField("Slug", unique=True, blank=True)
    short_name  = models.CharField("Qisqa nomi / Badge", max_length=100, blank=True)
    icon        = models.CharField("Emoji", max_length=10, default="🎓")
    image       = models.ImageField("Rasm", upload_to="faculties/", blank=True, null=True)
    description = models.TextField("Tavsif")
    degree      = models.CharField("Daraja", max_length=20, choices=DEGREE_CHOICES, default="bachelor")
    study_forms = models.CharField("O'qish shakllari", max_length=200,
                                   blank=True, default="Kunduzgi, Kechki, Sirtqi")
    duration    = models.PositiveIntegerField("O'qish muddati (yil)", default=4)
    order       = models.PositiveIntegerField("Tartib", default=0)
    is_active   = models.BooleanField("Faol", default=True)

    class Meta:
        verbose_name = "Yo'nalish"
        verbose_name_plural = "Yo'nalishlar"
        ordering = ["order"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug, n = base, 1
            while Faculty.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"; n += 1
            self.slug = slug
        super().save(*args, **kwargs)


# ─── Teacher ─────────────────────────────────────────────────────────────────
class Teacher(models.Model):
    full_name  = models.CharField("To'liq ism", max_length=200)
    slug       = models.SlugField("Slug", unique=True, blank=True)
    position   = models.CharField("Lavozim", max_length=200, blank=True)
    department = models.CharField("Kafedra", max_length=200, blank=True)
    faculty    = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="teachers", verbose_name="Yo'nalish")
    kafedra    = models.ForeignKey("Department", on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="teachers", verbose_name="Kafedra")
    photo      = models.ImageField("Foto", upload_to="teachers/", blank=True, null=True)
    bio        = models.TextField("Biografiya", blank=True)
    email      = models.EmailField("Email", blank=True)
    phone      = models.CharField("Telefon", max_length=30, blank=True)
    linkedin   = models.URLField("LinkedIn", blank=True)
    experience = models.PositiveIntegerField("Tajriba (yil)", default=0)
    order      = models.PositiveIntegerField("Tartib", default=0)
    is_active  = models.BooleanField("Faol", default=True)

    class Meta:
        verbose_name = "O'qituvchi"
        verbose_name_plural = "O'qituvchilar"
        ordering = ["order", "full_name"]

    def __str__(self):
        return f"{self.full_name} — {self.position}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.full_name)
            slug, n = base, 1
            while Teacher.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"; n += 1
            self.slug = slug
        super().save(*args, **kwargs)


# ─── News ─────────────────────────────────────────────────────────────────────
class NewsCategory(models.Model):
    name  = models.CharField("Nomi", max_length=100)
    slug  = models.SlugField("Slug", unique=True, blank=True)
    color = models.CharField("Rang", max_length=30, default="#3b82f6")

    class Meta:
        verbose_name = "Yangilik kategoriyasi"
        verbose_name_plural = "Yangilik kategoriyalari"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class News(models.Model):
    title       = models.CharField("Sarlavha", max_length=300)
    slug        = models.SlugField("Slug", unique=True, blank=True)
    category    = models.ForeignKey(NewsCategory, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="news", verbose_name="Kategoriya")
    image       = models.ImageField("Rasm", upload_to="news/")
    short_text  = models.TextField("Qisqa matn", max_length=500)
    body        = models.TextField("To'liq matn")
    author      = models.CharField("Muallif", max_length=200, blank=True)
    views       = models.PositiveIntegerField("Ko'rishlar", default=0)
    is_active   = models.BooleanField("Faol", default=True)
    is_featured = models.BooleanField("Asosiy yangilik", default=False)
    created_at  = models.DateTimeField("Yaratilgan", auto_now_add=True)
    updated_at  = models.DateTimeField("Yangilangan", auto_now=True)

    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug, n = base, 1
            while News.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"; n += 1
            self.slug = slug
        super().save(*args, **kwargs)


class NewsImage(models.Model):
    news    = models.ForeignKey(News, on_delete=models.CASCADE, related_name="images", verbose_name="Yangilik")
    image   = models.ImageField("Rasm", upload_to="news/gallery/")
    caption = models.CharField("Izoh", max_length=300, blank=True)
    order   = models.PositiveIntegerField("Tartib", default=0)

    class Meta:
        verbose_name = "Yangilik rasmi"
        verbose_name_plural = "Yangilik rasmlari"
        ordering = ["order"]

    def __str__(self):
        return f"{self.news.title} #{self.order}"


# ─── Event ────────────────────────────────────────────────────────────────────
class Event(models.Model):
    title       = models.CharField("Sarlavha", max_length=300)
    slug        = models.SlugField("Slug", unique=True, blank=True)
    image       = models.ImageField("Rasm", upload_to="events/", blank=True, null=True)
    description = models.TextField("Qisqa tavsif", blank=True)
    body        = models.TextField("To'liq matn", blank=True)
    location    = models.CharField("Joyi", max_length=200, blank=True)
    event_date  = models.DateTimeField("Tadbir sanasi")
    is_active   = models.BooleanField("Faol", default=True)
    views       = models.PositiveIntegerField("Ko'rishlar", default=0)
    created_at  = models.DateTimeField("Yaratilgan", auto_now_add=True)

    class Meta:
        verbose_name = "Tadbir"
        verbose_name_plural = "Tadbirlar"
        ordering = ["-event_date"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug, n = base, 1
            while Event.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"; n += 1
            self.slug = slug
        super().save(*args, **kwargs)


class EventImage(models.Model):
    event   = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="images", verbose_name="Tadbir")
    image   = models.ImageField("Rasm", upload_to="events/gallery/")
    caption = models.CharField("Izoh", max_length=300, blank=True)
    order   = models.PositiveIntegerField("Tartib", default=0)

    class Meta:
        verbose_name = "Tadbir rasmi"
        verbose_name_plural = "Tadbir rasmlari"
        ordering = ["order"]

    def __str__(self):
        return f"{self.event.title} #{self.order}"


# ─── Gallery ──────────────────────────────────────────────────────────────────
class Gallery(models.Model):
    title       = models.CharField("Album nomi", max_length=200)
    slug        = models.SlugField("Slug", unique=True, blank=True)
    cover       = models.ImageField("Muqova rasmi", upload_to="gallery/covers/", blank=True, null=True)
    description = models.TextField("Tavsif", blank=True)
    is_active   = models.BooleanField("Faol", default=True)
    created_at  = models.DateTimeField("Yaratilgan", auto_now_add=True)

    class Meta:
        verbose_name = "Galereya albomi"
        verbose_name_plural = "Galereya albumlari"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE,
                                related_name="images", verbose_name="Album")
    image   = models.ImageField("Rasm", upload_to="gallery/photos/")
    caption = models.CharField("Izoh", max_length=200, blank=True)
    order   = models.PositiveIntegerField("Tartib", default=0)

    class Meta:
        verbose_name = "Galereya rasmi"
        verbose_name_plural = "Galereya rasmlari"
        ordering = ["order"]

    def __str__(self):
        return f"{self.gallery.title} — #{self.order}"


# ─── FAQ ──────────────────────────────────────────────────────────────────────
class FAQ(models.Model):
    question  = models.CharField("Savol", max_length=400)
    answer    = models.TextField("Javob")
    order     = models.PositiveIntegerField("Tartib", default=0)
    is_active = models.BooleanField("Faol", default=True)

    class Meta:
        verbose_name = "FAQ (Savol-javob)"
        verbose_name_plural = "FAQ (Savol-javoblar)"
        ordering = ["order"]

    def __str__(self):
        return self.question


# ─── Partner ──────────────────────────────────────────────────────────────────
class Partner(models.Model):
    name      = models.CharField("Nomi", max_length=200)
    logo      = models.ImageField("Logo", upload_to="partners/")
    website   = models.URLField("Veb-sayt", blank=True)
    order     = models.PositiveIntegerField("Tartib", default=0)
    is_active = models.BooleanField("Faol", default=True)

    class Meta:
        verbose_name = "Hamkor"
        verbose_name_plural = "Hamkorlar"
        ordering = ["order"]

    def __str__(self):
        return self.name


# ─── Leadership (Rahbariyat) ──────────────────────────────────────────────────
class Leadership(models.Model):
    full_name       = models.CharField("To'liq ism", max_length=200)
    rank            = models.CharField("Unvon (qisqa)", max_length=100, blank=True,
                                       help_text="Masalan: Rektor, Prorektor")
    position        = models.CharField("Lavozim (to'liq)", max_length=300)
    qualification   = models.CharField("Ilmiy daraja", max_length=300, blank=True)
    photo           = models.ImageField("Foto", upload_to="leadership/", blank=True, null=True)
    bio             = models.TextField("Biografiya", blank=True)
    email           = models.EmailField("Email", blank=True)
    phone           = models.CharField("Telefon", max_length=30, blank=True)
    reception_days  = models.CharField("Qabul kunlari", max_length=200, blank=True,
                                        help_text="Masalan: Seshanba, Payshanba, Juma")
    reception_time  = models.CharField("Qabul vaqti", max_length=100, blank=True,
                                        help_text="Masalan: 15:00 – 16:00")
    order           = models.PositiveIntegerField("Tartib", default=0)
    is_active       = models.BooleanField("Faol", default=True)

    class Meta:
        verbose_name = "Rahbar"
        verbose_name_plural = "Rahbariyat"
        ordering = ["order"]

    def __str__(self):
        return f"{self.full_name} — {self.position}"


# ─── Department (Kafedra) ─────────────────────────────────────────────────────
class Department(models.Model):
    name        = models.CharField("Kafedra nomi", max_length=300)
    slug        = models.SlugField("Slug", unique=True, blank=True)
    head        = models.CharField("Kafedra mudiri", max_length=200, blank=True)
    description = models.TextField("Tavsif", blank=True)
    image       = models.ImageField("Rasm", upload_to="departments/", blank=True, null=True)
    faculty     = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="departments", verbose_name="Yo'nalish")
    order       = models.PositiveIntegerField("Tartib", default=0)
    is_active   = models.BooleanField("Faol", default=True)

    class Meta:
        verbose_name = "Kafedra"
        verbose_name_plural = "Kafedralar"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug, n = base, 1
            while Department.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"; n += 1
            self.slug = slug
        super().save(*args, **kwargs)


# ─── Center (Markazlar va bo'limlar) ──────────────────────────────────────────
class Center(models.Model):
    name        = models.CharField("Nomi", max_length=300)
    slug        = models.SlugField("Slug", unique=True, blank=True)
    icon        = models.CharField("Emoji", max_length=10, default="🏢")
    head        = models.CharField("Rahbar ismi", max_length=200, blank=True)
    head_role   = models.CharField("Rahbar lavozimi", max_length=300, blank=True)
    head_phone  = models.CharField("Telefon", max_length=30, blank=True)
    head_email  = models.EmailField("Email", blank=True)
    work_hours  = models.CharField("Ish vaqti", max_length=200, blank=True,
                                    help_text="Masalan: Dushanbidan Jumagacha 10:00–15:00")
    description = models.TextField("Tavsif", blank=True)
    image       = models.ImageField("Rasm (rahbar foto)", upload_to="centers/", blank=True, null=True)
    order       = models.PositiveIntegerField("Tartib", default=0)
    is_active   = models.BooleanField("Faol", default=True)

    class Meta:
        verbose_name = "Markaz / Bo'lim"
        verbose_name_plural = "Markazlar va bo'limlar"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug, n = base, 1
            while Center.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"; n += 1
            self.slug = slug
        super().save(*args, **kwargs)


# ─── Static Page ─────────────────────────────────────────────────────────────
class StaticPage(models.Model):
    title      = models.CharField("Sarlavha", max_length=300)
    slug       = models.SlugField("Slug", unique=True)
    body       = models.TextField("Mazmun (HTML)", blank=True)
    is_active  = models.BooleanField("Faol", default=True)
    updated_at = models.DateTimeField("Yangilangan", auto_now=True)

    class Meta:
        verbose_name = "Statik sahifa"
        verbose_name_plural = "Statik sahifalar"
        ordering = ["slug"]

    def __str__(self):
        return self.title


# ─── Scientific Articles ─────────────────────────────────────────────────────
class ArticleCategory(models.Model):
    name = models.CharField("Nomi", max_length=100)
    slug = models.SlugField("Slug", unique=True, blank=True)

    class Meta:
        verbose_name = "Maqola kategoriyasi"
        verbose_name_plural = "Maqola kategoriyalari"
        ordering = ["name"]

    def __str__(self): return self.name

    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.name)
        super().save(*args, **kwargs)


def _unique_slug(Model, base):
    slug, n = base, 1
    while Model.objects.filter(slug=slug).exists():
        slug = f"{base}-{n}"; n += 1
    return slug


class ScientificArticle(models.Model):
    LANG = [('uz', "O'zbek"), ('ru', 'Русский'), ('en', 'English')]
    title          = models.CharField("Sarlavha", max_length=300)
    slug           = models.SlugField("Slug", unique=True, blank=True)
    authors        = models.CharField("Mualliflar", max_length=400)
    journal_name   = models.CharField("Jurnal nomi", max_length=300, blank=True)
    published_date = models.DateField("Nashr sanasi", null=True, blank=True)
    abstract       = models.TextField("Annotatsiya", blank=True)
    category       = models.ForeignKey(ArticleCategory, on_delete=models.SET_NULL,
                                       null=True, blank=True, related_name="articles")
    pdf_file       = models.FileField("PDF fayl", upload_to="articles/pdf/", blank=True, null=True)
    cover_image    = models.ImageField("Muqova rasm", upload_to="articles/covers/", blank=True, null=True)
    doi_url        = models.URLField("DOI/Havola", blank=True)
    language       = models.CharField("Til", max_length=5, choices=LANG, default='uz')
    is_active      = models.BooleanField("Faol", default=True)
    views          = models.PositiveIntegerField("Ko'rishlar", default=0)
    created_at     = models.DateTimeField("Yaratilgan", auto_now_add=True)

    class Meta:
        verbose_name = "Ilmiy maqola"
        verbose_name_plural = "Ilmiy maqolalar"
        ordering = ["-published_date", "-created_at"]

    def __str__(self): return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _unique_slug(ScientificArticle, slugify(self.title) or "article")
        super().save(*args, **kwargs)


# ─── Dissertations ────────────────────────────────────────────────────────────
class Dissertation(models.Model):
    DEGREE = [('phd', 'PhD'), ('dsc', 'DSc'), ('candidate', 'Fan nomzodi')]
    title        = models.CharField("Sarlavha", max_length=400)
    slug         = models.SlugField("Slug", unique=True, blank=True)
    author       = models.CharField("Muallif", max_length=200)
    supervisor   = models.CharField("Ilmiy rahbar", max_length=200, blank=True)
    specialty    = models.CharField("Mutaxassislik", max_length=300, blank=True)
    degree       = models.CharField("Daraja", max_length=20, choices=DEGREE, default='phd')
    defense_date = models.DateField("Himoya sanasi", null=True, blank=True)
    abstract     = models.TextField("Annotatsiya", blank=True)
    faculty      = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name="dissertations")
    pdf_file     = models.FileField("PDF fayl", upload_to="dissertations/", blank=True, null=True)
    cover_image  = models.ImageField("Muqova rasm", upload_to="dissertations/covers/", blank=True, null=True)
    is_active    = models.BooleanField("Faol", default=True)
    views        = models.PositiveIntegerField("Ko'rishlar", default=0)
    created_at   = models.DateTimeField("Yaratilgan", auto_now_add=True)

    class Meta:
        verbose_name = "Dissertatsiya"
        verbose_name_plural = "Dissertatsiyalar"
        ordering = ["-defense_date", "-created_at"]

    def __str__(self): return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(f"{self.author}-{self.title[:60]}") or "dissertation"
            self.slug = _unique_slug(Dissertation, base)
        super().save(*args, **kwargs)


# ─── Conferences ──────────────────────────────────────────────────────────────
class Conference(models.Model):
    title            = models.CharField("Nomi", max_length=300)
    slug             = models.SlugField("Slug", unique=True, blank=True)
    description      = models.TextField("Tavsif", blank=True)
    start_date       = models.DateTimeField("Boshlanish sanasi")
    end_date         = models.DateTimeField("Tugash sanasi", null=True, blank=True)
    location         = models.CharField("Joyi", max_length=200, blank=True)
    poster_image     = models.ImageField("Poster rasm", upload_to="conferences/posters/", blank=True, null=True)
    cover_image      = models.ImageField("Muqova rasm", upload_to="conferences/covers/", blank=True, null=True)
    pdf_file         = models.FileField("Dastur (PDF)", upload_to="conferences/programs/", blank=True, null=True)
    registration_url = models.URLField("Roʻyxatdan oʻtish havola", blank=True)
    is_active        = models.BooleanField("Faol", default=True)
    views            = models.PositiveIntegerField("Ko'rishlar", default=0)
    created_at       = models.DateTimeField("Yaratilgan", auto_now_add=True)

    class Meta:
        verbose_name = "Konferensiya"
        verbose_name_plural = "Konferensiyalar"
        ordering = ["-start_date"]

    def __str__(self): return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _unique_slug(Conference, slugify(self.title) or "conference")
        super().save(*args, **kwargs)


# ─── Contests ─────────────────────────────────────────────────────────────────
class Contest(models.Model):
    title       = models.CharField("Nomi", max_length=300)
    slug        = models.SlugField("Slug", unique=True, blank=True)
    description = models.TextField("Tavsif", blank=True)
    deadline    = models.DateTimeField("Muddati", null=True, blank=True)
    cover_image = models.ImageField("Muqova rasm", upload_to="contests/", blank=True, null=True)
    pdf_file    = models.FileField("PDF (shartlar)", upload_to="contests/files/", blank=True, null=True)
    is_active   = models.BooleanField("Faol", default=True)
    views       = models.PositiveIntegerField("Ko'rishlar", default=0)
    created_at  = models.DateTimeField("Yaratilgan", auto_now_add=True)

    class Meta:
        verbose_name = "Tanlov"
        verbose_name_plural = "Tanlovlar"
        ordering = ["-deadline", "-created_at"]

    def __str__(self): return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _unique_slug(Contest, slugify(self.title) or "contest")
        super().save(*args, **kwargs)


# ─── Video Lessons ────────────────────────────────────────────────────────────
class VideoLesson(models.Model):
    title       = models.CharField("Nomi", max_length=300)
    slug        = models.SlugField("Slug", unique=True, blank=True)
    description = models.TextField("Tavsif", blank=True)
    youtube_url = models.URLField("YouTube havola", blank=True)
    cover_image = models.ImageField("Thumbnail", upload_to="videos/", blank=True, null=True)
    faculty     = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="videos")
    duration    = models.CharField("Davomiyligi", max_length=20, blank=True)
    is_active   = models.BooleanField("Faol", default=True)
    views       = models.PositiveIntegerField("Ko'rishlar", default=0)
    created_at  = models.DateTimeField("Yaratilgan", auto_now_add=True)

    class Meta:
        verbose_name = "Video dars"
        verbose_name_plural = "Video darslar"
        ordering = ["-created_at"]

    def __str__(self): return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _unique_slug(VideoLesson, slugify(self.title) or "video")
        super().save(*args, **kwargs)


# ─── Talented Students ────────────────────────────────────────────────────────
class TalentedStudent(models.Model):
    full_name   = models.CharField("F.I.O.", max_length=200)
    slug        = models.SlugField("Slug", unique=True, blank=True)
    faculty     = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="talented_students")
    achievement = models.CharField("Yutuq/Unvon", max_length=300)
    year        = models.PositiveIntegerField("Yil", default=2025)
    photo       = models.ImageField("Foto", upload_to="talented/", blank=True, null=True)
    description = models.TextField("Tavsif", blank=True)
    is_active   = models.BooleanField("Faol", default=True)
    created_at  = models.DateTimeField("Yaratilgan", auto_now_add=True)

    class Meta:
        verbose_name = "Iqtidorli talaba"
        verbose_name_plural = "Iqtidorli talabalar"
        ordering = ["-year", "full_name"]

    def __str__(self): return f"{self.full_name} — {self.achievement}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _unique_slug(TalentedStudent, slugify(self.full_name) or "student")
        super().save(*args, **kwargs)


# ─── Journal Issues ───────────────────────────────────────────────────────────
class JournalIssue(models.Model):
    title       = models.CharField("Son nomi", max_length=300)
    slug        = models.SlugField("Slug", unique=True, blank=True)
    year        = models.PositiveIntegerField("Yil")
    issue_number= models.PositiveIntegerField("Son raqami")
    cover_image = models.ImageField("Muqova rasm", upload_to="journal/covers/", blank=True, null=True)
    pdf_file    = models.FileField("PDF fayl", upload_to="journal/files/", blank=True, null=True)
    description = models.TextField("Tavsif", blank=True)
    is_active   = models.BooleanField("Faol", default=True)
    created_at  = models.DateTimeField("Yaratilgan", auto_now_add=True)

    class Meta:
        verbose_name = "Ilmiy jurnal soni"
        verbose_name_plural = "Ilmiy jurnal sonlari"
        ordering = ["-year", "-issue_number"]

    def __str__(self): return f"{self.year}-yil, {self.issue_number}-son"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _unique_slug(JournalIssue, f"{self.year}-{self.issue_number}-son")
        super().save(*args, **kwargs)


# ─── Schedule Files ───────────────────────────────────────────────────────────
class ScheduleFile(models.Model):
    SEM = [(1, "1-semestr"), (2, "2-semestr")]
    title         = models.CharField("Nomi", max_length=300)
    slug          = models.SlugField("Slug", unique=True, blank=True)
    faculty       = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name="schedules")
    academic_year = models.CharField("O'quv yili", max_length=20, default="2025-2026")
    semester      = models.PositiveSmallIntegerField("Semestr", choices=SEM, default=1)
    file          = models.FileField("Fayl (PDF/Excel)", upload_to="schedules/")
    is_active     = models.BooleanField("Faol", default=True)
    created_at    = models.DateTimeField("Yaratilgan", auto_now_add=True)

    class Meta:
        verbose_name = "Dars jadvali"
        verbose_name_plural = "Dars jadvallari"
        ordering = ["-academic_year", "-semester"]

    def __str__(self): return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _unique_slug(ScheduleFile, slugify(self.title) or "schedule")
        super().save(*args, **kwargs)


# ─── Library Resources ────────────────────────────────────────────────────────
class LibraryResource(models.Model):
    RTYPE = [('book', 'Kitob'), ('article', 'Maqola'),
             ('manual', "Qo'llanma"), ('dissertation', 'Dissertatsiya'), ('other', 'Boshqa')]
    title         = models.CharField("Nomi", max_length=300)
    slug          = models.SlugField("Slug", unique=True, blank=True)
    authors       = models.CharField("Mualliflar", max_length=400, blank=True)
    description   = models.TextField("Tavsif", blank=True)
    cover_image   = models.ImageField("Muqova rasm", upload_to="library/covers/", blank=True, null=True)
    file          = models.FileField("PDF fayl", upload_to="library/files/", blank=True, null=True)
    external_url  = models.URLField("Tashqi havola", blank=True)
    resource_type = models.CharField("Turi", max_length=20, choices=RTYPE, default='book')
    is_active     = models.BooleanField("Faol", default=True)
    views         = models.PositiveIntegerField("Ko'rishlar", default=0)
    created_at    = models.DateTimeField("Yaratilgan", auto_now_add=True)

    class Meta:
        verbose_name = "Kutubxona resursi"
        verbose_name_plural = "Elektron kutubxona"
        ordering = ["-created_at"]

    def __str__(self): return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _unique_slug(LibraryResource, slugify(self.title) or "resource")
        super().save(*args, **kwargs)


# ─── Contact Message ──────────────────────────────────────────────────────────
class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ("new",      "Yangi"),
        ("read",     "O'qilgan"),
        ("answered", "Javob berilgan"),
    ]

    first_name = models.CharField("Ism", max_length=100)
    last_name  = models.CharField("Familiya", max_length=100)
    phone      = models.CharField("Telefon", max_length=30, blank=True)
    email      = models.EmailField("Email", blank=True)
    direction  = models.CharField("Qiziqtirgan yo'nalish", max_length=200, blank=True)
    message    = models.TextField("Xabar", blank=True)
    status     = models.CharField("Holat", max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField("Yuborilgan", auto_now_add=True)

    class Meta:
        verbose_name = "Aloqa xabari"
        verbose_name_plural = "Aloqa xabarlari"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} — {self.created_at:%d.%m.%Y %H:%M}"
