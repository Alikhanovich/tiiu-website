from django.db import migrations

REMOVE_SLUGS = [
    'ilmiy-maqolalar', 'dissertatsiyalar', 'ilmiy-jurnal',
    'konferensiyalar', 'dars-jadvali', 'iqtidorli-talabalar',
    'tanlovlar', 'elektron-kutubxona', 'video-darslar',
]


def remove_pages(apps, schema_editor):
    StaticPage = apps.get_model('main', 'StaticPage')
    StaticPage.objects.filter(slug__in=REMOVE_SLUGS).delete()


class Migration(migrations.Migration):
    dependencies = [('main', '0010_new_content_models')]
    operations = [migrations.RunPython(remove_pages, migrations.RunPython.noop)]
