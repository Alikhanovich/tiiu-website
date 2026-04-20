from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_event_body_views'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaticPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Sarlavha')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('body', models.TextField(blank=True, verbose_name='Mazmun (HTML)')),
                ('is_active', models.BooleanField(default=True, verbose_name='Faol')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan')),
            ],
            options={
                'verbose_name': 'Statik sahifa',
                'verbose_name_plural': 'Statik sahifalar',
                'ordering': ['slug'],
            },
        ),
    ]
