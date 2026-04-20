#!/usr/bin/env bash
# Render build script
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate --noinput

# Create superuser automatically if it doesn't exist
python manage.py shell -c "
from django.contrib.auth.models import User
import os
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'Abboskhon_Alikhanovich')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@tiiu.uz')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'Alikhanovich05')
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Superuser {username} created!')
else:
    print(f'Superuser {username} already exists.')
"
