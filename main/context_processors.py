from .models import SiteSettings, Faculty, Department


def site_settings(request):
    return {
        "settings": SiteSettings.get(),
        "nav_faculties":    Faculty.objects.filter(is_active=True)[:10],
        "nav_departments":  Department.objects.filter(is_active=True)[:8],
    }
