#!/usr/bin/env bash
# Render START script (runtime). The database IS reachable here, so
# migrations and superuser creation happen at startup — not during build.
set -o errexit

python manage.py migrate --noinput

# Re-seed content from the committed fixture. build.sh already did this, so
# normally every object here is just overwritten with identical values; this is
# the safety net for the case where the DB was reset between build and start.
# Failure is not fatal (the build-time load is the authoritative one), but it
# must be impossible to miss in the logs.
python manage.py loaddata main/fixtures/initial_data.json \
  || echo "!!!!! FIXTURE LOAD FAILED AT RUNTIME — check content on the live site !!!!!"

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
