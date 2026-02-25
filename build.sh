#!/usr/bin/env bash
# build.sh — Render ejecuta este script al desplegar el backend

set -o errexit  # salir si cualquier comando falla

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate