#!/usr/bin/env bash
# Render BUILD script.
# NOTE: The database is NOT reachable during the build phase on Render
# (the private network is only available at runtime). DB-touching commands
# — migrate, superuser creation — run at RUNTIME via start.sh instead.
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
