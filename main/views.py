from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import (
    SiteSettings, Slider, Faculty, Teacher,
    NewsCategory, News, Event,
    Gallery, GalleryImage, FAQ, Partner, ContactMessage,
    Leadership, Department, Center, StaticPage,
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
