from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from .models import (
    SiteSettings, Slider, Faculty, Teacher,
    NewsCategory, News, Event,
    Gallery, GalleryImage, FAQ, Partner, ContactMessage,
    Leadership, Department, Center, StaticPage,
    ArticleCategory, ScientificArticle, Dissertation, Conference,
    Contest, VideoLesson, TalentedStudent, JournalIssue,
    ScheduleFile, LibraryResource,
)


def index(request):
    ctx = {
        "sliders":   Slider.objects.filter(is_active=True),
        "faculties": Faculty.objects.filter(is_active=True),
        "news":      News.objects.filter(is_active=True)[:6],
        "featured":  News.objects.filter(is_active=True, is_featured=True).first(),
        "faqs":      FAQ.objects.filter(is_active=True),
        "partners":  Partner.objects.filter(is_active=True),
        "events":    Event.objects.filter(is_active=True)[:3],
    }
    return render(request, "main/index.html", ctx)


def about(request):
    ctx = {
        "teachers": Teacher.objects.filter(is_active=True),
        "faculties": Faculty.objects.filter(is_active=True),
    }
    return render(request, "main/about.html", ctx)


def faculties(request):
    ctx = {"faculties": Faculty.objects.filter(is_active=True)}
    return render(request, "main/faculties.html", ctx)


def faculty_detail(request, slug):
    faculty = get_object_or_404(Faculty, slug=slug, is_active=True)
    teachers = faculty.teachers.filter(is_active=True)
    ctx = {"faculty": faculty, "teachers": teachers}
    return render(request, "main/faculty_detail.html", ctx)


def news_list(request):
    category_slug = request.GET.get("cat")
    categories = NewsCategory.objects.all()
    news_qs = News.objects.filter(is_active=True)
    if category_slug:
        news_qs = news_qs.filter(category__slug=category_slug)
    ctx = {
        "news_list":  news_qs,
        "categories": categories,
        "active_cat": category_slug,
    }
    return render(request, "main/news_list.html", ctx)


def news_detail(request, slug):
    article = get_object_or_404(News, slug=slug, is_active=True)
    article.views += 1
    article.save(update_fields=["views"])
    related = News.objects.filter(is_active=True).exclude(pk=article.pk)[:3]
    ctx = {"article": article, "related": related}
    return render(request, "main/news_detail.html", ctx)


def events(request):
    ctx = {"events": Event.objects.filter(is_active=True)}
    return render(request, "main/events.html", ctx)


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug, is_active=True)
    Event.objects.filter(pk=event.pk).update(views=event.views + 1)
    related = Event.objects.filter(is_active=True).exclude(pk=event.pk)[:4]
    ctx = {"event": event, "related": related, "images": event.images.all()}
    return render(request, "main/event_detail.html", ctx)


def gallery(request):
    ctx = {"galleries": Gallery.objects.filter(is_active=True)}
    return render(request, "main/gallery.html", ctx)


def gallery_detail(request, slug):
    album = get_object_or_404(Gallery, slug=slug, is_active=True)
    ctx = {"album": album, "images": album.images.all()}
    return render(request, "main/gallery_detail.html", ctx)


def contact(request):
    ctx = {"faqs": FAQ.objects.filter(is_active=True)}
    return render(request, "main/contact.html", ctx)


@require_POST
def contact_submit(request):
    data = request.POST
    ContactMessage.objects.create(
        first_name=data.get("first_name", ""),
        last_name=data.get("last_name", ""),
        phone=data.get("phone", ""),
        email=data.get("email", ""),
        direction=data.get("direction", ""),
        message=data.get("message", ""),
    )
    return JsonResponse({"ok": True})


def teachers(request):
    ctx = {"teachers": Teacher.objects.filter(is_active=True)}
    return render(request, "main/teachers.html", ctx)


def leadership(request):
    ctx = {"leaders": Leadership.objects.filter(is_active=True)}
    return render(request, "main/leadership.html", ctx)


def departments(request):
    depts = Department.objects.filter(is_active=True).prefetch_related("teachers")
    ctx = {"departments": depts}
    return render(request, "main/departments.html", ctx)


def centers(request):
    ctx = {"centers": Center.objects.filter(is_active=True)}
    return render(request, "main/centers.html", ctx)


def static_page(request, slug):
    page = get_object_or_404(StaticPage, slug=slug, is_active=True)
    return render(request, "main/static_page.html", {"page": page})


def _paginate(request, qs, per=10):
    p = Paginator(qs, per)
    return p.get_page(request.GET.get('page', 1))


# ── Ilm-fan ───────────────────────────────────────────────────────────────────
def articles_list(request):
    qs = ScientificArticle.objects.filter(is_active=True)
    cat_slug = request.GET.get('cat')
    q = request.GET.get('q', '').strip()
    year = request.GET.get('year')
    if cat_slug: qs = qs.filter(category__slug=cat_slug)
    if q: qs = qs.filter(title__icontains=q) | qs.filter(authors__icontains=q)
    if year: qs = qs.filter(published_date__year=year)
    cats = ArticleCategory.objects.all()
    years = ScientificArticle.objects.filter(is_active=True).dates('published_date', 'year')
    ctx = {'articles': _paginate(request, qs), 'categories': cats, 'years': years,
           'active_cat': cat_slug, 'q': q, 'active_year': year}
    return render(request, 'main/articles_list.html', ctx)


def article_detail(request, slug):
    obj = get_object_or_404(ScientificArticle, slug=slug, is_active=True)
    ScientificArticle.objects.filter(pk=obj.pk).update(views=obj.views + 1)
    related = ScientificArticle.objects.filter(is_active=True).exclude(pk=obj.pk)[:4]
    return render(request, 'main/article_detail.html', {'obj': obj, 'related': related})


def dissertations_list(request):
    qs = Dissertation.objects.filter(is_active=True)
    q = request.GET.get('q', '').strip()
    year = request.GET.get('year')
    degree = request.GET.get('degree')
    if q: qs = qs.filter(title__icontains=q) | qs.filter(author__icontains=q)
    if year: qs = qs.filter(defense_date__year=year)
    if degree: qs = qs.filter(degree=degree)
    years = Dissertation.objects.filter(is_active=True).dates('defense_date', 'year')
    ctx = {'items': _paginate(request, qs), 'years': years, 'q': q,
           'active_year': year, 'degree': degree}
    return render(request, 'main/dissertations_list.html', ctx)


def dissertation_detail(request, slug):
    obj = get_object_or_404(Dissertation, slug=slug, is_active=True)
    Dissertation.objects.filter(pk=obj.pk).update(views=obj.views + 1)
    related = Dissertation.objects.filter(is_active=True).exclude(pk=obj.pk)[:4]
    return render(request, 'main/dissertation_detail.html', {'obj': obj, 'related': related})


def conferences_list(request):
    from django.utils import timezone
    now = timezone.now()
    tab = request.GET.get('tab', 'upcoming')
    qs = Conference.objects.filter(is_active=True)
    qs = qs.filter(start_date__gte=now) if tab == 'upcoming' else qs.filter(start_date__lt=now)
    ctx = {'items': _paginate(request, qs), 'tab': tab}
    return render(request, 'main/conferences_list.html', ctx)


def conference_detail(request, slug):
    obj = get_object_or_404(Conference, slug=slug, is_active=True)
    Conference.objects.filter(pk=obj.pk).update(views=obj.views + 1)
    return render(request, 'main/conference_detail.html', {'obj': obj})


def contests_list(request):
    qs = Contest.objects.filter(is_active=True)
    ctx = {'items': _paginate(request, qs)}
    return render(request, 'main/contests_list.html', ctx)


def contest_detail(request, slug):
    obj = get_object_or_404(Contest, slug=slug, is_active=True)
    Contest.objects.filter(pk=obj.pk).update(views=obj.views + 1)
    return render(request, 'main/contest_detail.html', {'obj': obj})


def journal_list(request):
    qs = JournalIssue.objects.filter(is_active=True)
    ctx = {'items': _paginate(request, qs, per=12)}
    return render(request, 'main/journal_list.html', ctx)


def journal_detail(request, slug):
    obj = get_object_or_404(JournalIssue, slug=slug, is_active=True)
    return render(request, 'main/journal_detail.html', {'obj': obj})


# ── Talabalarga ───────────────────────────────────────────────────────────────
def video_lessons_list(request):
    qs = VideoLesson.objects.filter(is_active=True)
    fac = request.GET.get('faculty')
    if fac: qs = qs.filter(faculty__slug=fac)
    faculties = Faculty.objects.filter(is_active=True)
    ctx = {'items': _paginate(request, qs), 'faculties': faculties, 'active_fac': fac}
    return render(request, 'main/video_lessons_list.html', ctx)


def video_lesson_detail(request, slug):
    obj = get_object_or_404(VideoLesson, slug=slug, is_active=True)
    VideoLesson.objects.filter(pk=obj.pk).update(views=obj.views + 1)
    related = VideoLesson.objects.filter(is_active=True).exclude(pk=obj.pk)[:4]
    return render(request, 'main/video_lesson_detail.html', {'obj': obj, 'related': related})


def talented_students(request):
    qs = TalentedStudent.objects.filter(is_active=True)
    year = request.GET.get('year')
    fac = request.GET.get('faculty')
    if year: qs = qs.filter(year=year)
    if fac: qs = qs.filter(faculty__slug=fac)
    years = TalentedStudent.objects.filter(is_active=True).values_list('year', flat=True).distinct().order_by('-year')
    faculties = Faculty.objects.filter(is_active=True)
    ctx = {'items': _paginate(request, qs), 'years': years, 'faculties': faculties,
           'active_year': year, 'active_fac': fac}
    return render(request, 'main/talented_students.html', ctx)


def schedule_list(request):
    qs = ScheduleFile.objects.filter(is_active=True)
    yr = request.GET.get('year')
    fac = request.GET.get('faculty')
    if yr: qs = qs.filter(academic_year=yr)
    if fac: qs = qs.filter(faculty__slug=fac)
    years = ScheduleFile.objects.filter(is_active=True).values_list('academic_year', flat=True).distinct()
    faculties = Faculty.objects.filter(is_active=True)
    ctx = {'items': qs, 'years': years, 'faculties': faculties,
           'active_year': yr, 'active_fac': fac}
    return render(request, 'main/schedule_list.html', ctx)


def library_list(request):
    qs = LibraryResource.objects.filter(is_active=True)
    q = request.GET.get('q', '').strip()
    rtype = request.GET.get('type')
    if q: qs = qs.filter(title__icontains=q) | qs.filter(authors__icontains=q)
    if rtype: qs = qs.filter(resource_type=rtype)
    ctx = {'items': _paginate(request, qs), 'q': q, 'active_type': rtype,
           'types': LibraryResource.RTYPE}
    return render(request, 'main/library_list.html', ctx)


def library_detail(request, slug):
    obj = get_object_or_404(LibraryResource, slug=slug, is_active=True)
    LibraryResource.objects.filter(pk=obj.pk).update(views=obj.views + 1)
    return render(request, 'main/library_detail.html', {'obj': obj})


def sitemap(request):
    base = f"{request.scheme}://{request.get_host()}"
    urls = [
        ("", "daily",   "1.0"),
        ("about/",      "weekly", "0.8"),
        ("faculties/",  "weekly", "0.8"),
        ("news/",       "daily",  "0.9"),
        ("events/",     "weekly", "0.8"),
        ("gallery/",    "weekly", "0.7"),
        ("teachers/",   "monthly","0.6"),
        ("departments/","monthly","0.6"),
        ("centers/",    "monthly","0.6"),
        ("contact/",    "monthly","0.5"),
    ]
    items = "\n".join(
        f"  <url><loc>{base}/{u}</loc><changefreq>{cf}</changefreq><priority>{p}</priority></url>"
        for u, cf, p in urls
    )
    for n in News.objects.filter(is_active=True).values_list("slug", flat=True):
        items += f"\n  <url><loc>{base}/news/{n}/</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>"
    for n in Event.objects.filter(is_active=True).values_list("slug", flat=True):
        items += f"\n  <url><loc>{base}/events/{n}/</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>"
    for n in Faculty.objects.filter(is_active=True).values_list("slug", flat=True):
        items += f"\n  <url><loc>{base}/faculties/{n}/</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>"
    for n in StaticPage.objects.filter(is_active=True).values_list("slug", flat=True):
        items += f"\n  <url><loc>{base}/pages/{n}/</loc><changefreq>monthly</changefreq><priority>0.6</priority></url>"
    xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}\n</urlset>'
    return HttpResponse(xml, content_type="application/xml")
