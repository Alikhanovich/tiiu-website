from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SiteSettings, Slider, Faculty, Teacher,
    NewsCategory, News, Event,
    Gallery, GalleryImage, FAQ, Partner, ContactMessage,
    Leadership, Department, Center,
)


def img_preview(url, size=60):
    if url:
        return format_html(
            '<img src="{}" style="height:{}px;border-radius:6px;object-fit:cover"/>',
            url, size
        )
    return "—"


# ─── Site Settings ────────────────────────────────────────────────────────────
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Asosiy",            {"fields": ("site_name", "site_name_full", "logo", "favicon")}),
        ("Aloqa",             {"fields": ("address", "phone1", "phone2", "email", "work_hours")}),
        ("Ijtimoiy tarmoqlar",{"fields": ("facebook", "instagram", "telegram", "youtube")}),
        ("Statistika",        {"fields": ("founded_year", "student_count", "teacher_count", "direction_count")}),
        ("Hero bo'limi",      {"fields": ("hero_title", "hero_subtitle")}),
        ("Haqida",            {"fields": ("about_text",)}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ─── Slider ───────────────────────────────────────────────────────────────────
@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display       = ("title", "preview", "order", "is_active")
    list_editable      = ("order", "is_active")
    list_display_links = ("title",)

    def preview(self, obj):
        return img_preview(obj.image.url if obj.image else None)
    preview.short_description = "Ko'rinish"


# ─── Faculty ──────────────────────────────────────────────────────────────────
@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display       = ("icon", "name", "short_name", "degree", "duration", "order", "is_active")
    list_editable      = ("order", "is_active")
    list_display_links = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields      = ("name", "description")
    list_filter        = ("degree", "is_active")
    fieldsets = (
        ("Asosiy",     {"fields": ("name", "slug", "short_name", "icon", "image", "degree", "duration")}),
        ("Ma'lumot",   {"fields": ("description", "study_forms")}),
        ("Sozlamalar", {"fields": ("order", "is_active")}),
    )


# ─── Teacher ──────────────────────────────────────────────────────────────────
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display       = ("photo_preview", "full_name", "position", "kafedra", "experience", "is_active")
    list_editable      = ("is_active",)
    list_display_links = ("full_name",)
    list_filter        = ("is_active",)
    search_fields      = ("full_name", "position", "bio")
    prepopulated_fields = {"slug": ("full_name",)}
    fieldsets = (
        ("Shaxsiy",    {"fields": ("full_name", "slug", "photo", "position", "kafedra")}),
        ("Aloqa",      {"fields": ("email", "phone", "linkedin")}),
        ("Qo'shimcha", {"fields": ("bio", "experience", "order", "is_active")}),
    )

    def photo_preview(self, obj):
        return img_preview(obj.photo.url if obj.photo else None, size=50)
    photo_preview.short_description = "Foto"


# ─── News Category ────────────────────────────────────────────────────────────
@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display        = ("name", "slug", "color_badge")
    prepopulated_fields = {"slug": ("name",)}

    def color_badge(self, obj):
        return format_html(
            '<span style="background:{c};color:#fff;padding:3px 10px;border-radius:4px;font-size:12px">{c}</span>',
            c=obj.color,
        )
    color_badge.short_description = "Rang"


# ─── News ─────────────────────────────────────────────────────────────────────
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display       = ("img_prev", "title", "category", "author", "views", "is_featured", "is_active", "created_at")
    list_editable      = ("is_featured", "is_active")
    list_display_links = ("title",)
    list_filter        = ("is_active", "is_featured", "category")
    search_fields      = ("title", "short_text", "body", "author")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields    = ("views", "created_at", "updated_at")
    date_hierarchy     = "created_at"
    fieldsets = (
        ("Asosiy",     {"fields": ("title", "slug", "category", "image", "author")}),
        ("Matn",       {"fields": ("short_text", "body")}),
        ("Sozlamalar", {"fields": ("is_active", "is_featured", "views", "created_at", "updated_at")}),
    )

    def img_prev(self, obj):
        return img_preview(obj.image.url if obj.image else None)
    img_prev.short_description = "Rasm"


# ─── Event ────────────────────────────────────────────────────────────────────
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display       = ("img_prev", "title", "event_date", "location", "is_active")
    list_editable      = ("is_active",)
    list_display_links = ("title",)
    list_filter        = ("is_active",)
    search_fields      = ("title", "description", "location")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy     = "event_date"

    def img_prev(self, obj):
        return img_preview(obj.image.url if obj.image else None)
    img_prev.short_description = "Rasm"


# ─── Gallery ──────────────────────────────────────────────────────────────────
class GalleryImageInline(admin.TabularInline):
    model  = GalleryImage
    extra  = 3
    fields = ("image", "caption", "order")


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display       = ("cover_preview", "title", "image_count", "is_active", "created_at")
    list_editable      = ("is_active",)
    list_display_links = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    inlines            = [GalleryImageInline]

    def cover_preview(self, obj):
        return img_preview(obj.cover.url if obj.cover else None)
    cover_preview.short_description = "Muqova"

    def image_count(self, obj):
        return obj.images.count()
    image_count.short_description = "Rasmlar soni"


# ─── FAQ ──────────────────────────────────────────────────────────────────────
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display  = ("question", "order", "is_active")
    list_editable = ("order", "is_active")
    list_display_links = ("question",)
    search_fields = ("question", "answer")


# ─── Partner ──────────────────────────────────────────────────────────────────
@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display  = ("logo_preview", "name", "website", "order", "is_active")
    list_editable = ("order", "is_active")
    list_display_links = ("name",)

    def logo_preview(self, obj):
        return img_preview(obj.logo.url if obj.logo else None, size=40)
    logo_preview.short_description = "Logo"


# ─── Contact Message ──────────────────────────────────────────────────────────
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display       = ("name_col", "phone", "email", "direction", "status_badge", "created_at")
    list_display_links = ("name_col",)
    list_filter        = ("status",)
    search_fields      = ("first_name", "last_name", "phone", "email", "message")
    readonly_fields    = ("first_name", "last_name", "phone", "email",
                          "direction", "message", "created_at")
    date_hierarchy     = "created_at"
    actions            = ["mark_read", "mark_answered"]
    fieldsets = (
        ("Yuboruvchi", {"fields": ("first_name", "last_name", "phone", "email")}),
        ("Xabar",      {"fields": ("direction", "message")}),
        ("Holat",      {"fields": ("status", "created_at")}),
    )

    def name_col(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    name_col.short_description = "Ism Familiya"

    def status_badge(self, obj):
        colors = {"new": "#ef4444", "read": "#f59e0b", "answered": "#22c55e"}
        labels = {"new": "Yangi", "read": "O'qilgan", "answered": "Javob berilgan"}
        c = colors.get(obj.status, "#6b7280")
        l = labels.get(obj.status, obj.status)
        return format_html(
            '<span style="background:{c};color:#fff;padding:3px 12px;'
            'border-radius:50px;font-size:11px;font-weight:700">{l}</span>',
            c=c, l=l,
        )
    status_badge.short_description = "Holat"

    @admin.action(description="O'qilgan deb belgilash")
    def mark_read(self, request, queryset):
        queryset.update(status="read")

    @admin.action(description="Javob berilgan deb belgilash")
    def mark_answered(self, request, queryset):
        queryset.update(status="answered")

    def has_add_permission(self, request):
        return False


# ─── Leadership ───────────────────────────────────────────────────────────────
@admin.register(Leadership)
class LeadershipAdmin(admin.ModelAdmin):
    list_display       = ("photo_preview", "full_name", "rank", "position", "phone", "order", "is_active")
    list_editable      = ("order", "is_active")
    list_display_links = ("full_name",)
    search_fields      = ("full_name", "rank", "position", "email")
    fieldsets = (
        ("Shaxsiy ma'lumotlar", {
            "fields": ("photo", "full_name", "rank", "position", "qualification"),
            "description": "Unvon: Rektor, Prorektor va h.k. | Lavozim: to'liq tavsif",
        }),
        ("Aloqa", {
            "fields": ("phone", "email"),
        }),
        ("Qabul kunlari", {
            "fields": ("reception_days", "reception_time"),
            "description": "Masalan: Seshanba, Payshanba | 15:00 – 16:00",
        }),
        ("Qo'shimcha", {
            "fields": ("bio", "order", "is_active"),
            "classes": ("collapse",),
        }),
    )

    def photo_preview(self, obj):
        return img_preview(obj.photo.url if obj.photo else None, size=50)
    photo_preview.short_description = "Foto"


# ─── Department (Kafedra) ─────────────────────────────────────────────────────
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display        = ("name", "head", "teacher_count", "order", "is_active")
    list_editable       = ("order", "is_active")
    list_display_links  = ("name",)
    list_filter         = ("is_active",)
    search_fields       = ("name", "head", "description")
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        ("Asosiy",     {"fields": ("name", "slug", "head", "image")}),
        ("Ma'lumot",   {"fields": ("description",)}),
        ("Sozlamalar", {"fields": ("order", "is_active")}),
    )

    def teacher_count(self, obj):
        return obj.teachers.count()
    teacher_count.short_description = "O'qituvchilar"


# ─── Center (Markazlar va bo'limlar) ──────────────────────────────────────────
@admin.register(Center)
class CenterAdmin(admin.ModelAdmin):
    list_display        = ("photo_preview", "name", "head", "head_phone", "head_email", "order", "is_active")
    list_editable       = ("order", "is_active")
    list_display_links  = ("name",)
    search_fields       = ("name", "head", "head_role", "head_email", "description")
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        ("Bo'lim ma'lumotlari", {
            "fields": ("name", "slug", "icon", "description"),
            "description": "Bo'lim yoki markaz nomi va tavsifi",
        }),
        ("Rahbar", {
            "fields": ("image", "head", "head_role"),
            "description": "Rahbar rasmi, ismi va lavozimi",
        }),
        ("Aloqa", {
            "fields": ("head_phone", "head_email", "work_hours"),
        }),
        ("Sozlamalar", {
            "fields": ("order", "is_active"),
            "classes": ("collapse",),
        }),
    )

    def photo_preview(self, obj):
        return img_preview(obj.image.url if obj.image else None, size=50)
    photo_preview.short_description = "Foto"
