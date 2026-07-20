#!/usr/bin/env bash
# Render START script (runtime). The database IS reachable here, so
# migrations and superuser creation happen at startup — not during build.
set -o errexit

python manage.py migrate --noinput

# Seed all site content (teachers, news, leadership, settings, ...) from the
# committed fixture. Render's filesystem is ephemeral, so the SQLite DB is
# empty on every start — this repopulates it from git each time, which means
# production always mirrors the content you committed locally.
python manage.py loaddata main/fixtures/initial_data.json || echo "WARNING: fixture load failed — site will start with empty content."

# Create superuser only if env vars are explicitly set (idempotent).
python manage.py shell -c "
from django.contrib.auth import get_user_model
import os
User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', '')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '')
if not username or not password:
    print('DJANGO_SUPERUSER_USERNAME/PASSWORD not set - skipping superuser creation.')
elif not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print('Superuser ' + username + ' created!')
else:
    print('Superuser ' + username + ' already exists.')
"

exec gunicorn config.wsgi:application --workers 4 --timeout 120 --bind "0.0.0.0:${PORT:-8000}"
