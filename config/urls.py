from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.views.generic import RedirectView

ROBOTS = (
    "User-agent: *\n"
    "Disallow: /admin/\n"
    "Disallow: /panel/\n"
    "Sitemap: https://tiiu.uz/sitemap.xml\n"
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("panel/", include("panel.urls")),
    path("sw.js",        lambda r: HttpResponse("", content_type="application/javascript")),
    path("robots.txt",   lambda r: HttpResponse(ROBOTS, content_type="text/plain")),
    path("favicon.ico",  RedirectView.as_view(url="/static/img/favicon.png", permanent=True)),
    path("", include("main.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
