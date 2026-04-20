from django.db import migrations

SEED_PAGES = [
    ("Ilmiy faoliyat",                   "ilmiy-faoliyat"),
    ("Ilmiy maqolalar",                  "ilmiy-maqolalar"),
    ("Dissertatsiyalar",                 "dissertatsiyalar"),
    ("Ilmiy jurnal",                     "ilmiy-jurnal"),
    ("Konferensiyalar",                  "konferensiyalar"),
    ("Elektron Ta'lim Tizimi",           "elektron-talim-tizimi"),
    ("Dars Jadvali",                     "dars-jadvali"),
    ("Iqtidorli Talabalar",              "iqtidorli-talabalar"),
    ("Tanlovlar",                        "tanlovlar"),
    ("Elektron Kutubxona",               "elektron-kutubxona"),
    ("Talabalar O'rtasida So'rovnoma",   "sorovnoma"),
    ("Video Darslar",                    "video-darslar"),
]


def seed(apps, schema_editor):
    StaticPage = apps.get_model('main', 'StaticPage')
    for title, slug in SEED_PAGES:
        StaticPage.objects.get_or_create(slug=slug, defaults={'title': title})


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_staticpage'),
    ]

    operations = [
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
