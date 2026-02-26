#!/usr/bin/env bash
# build.sh — Render ejecuta este script al desplegar el backend

set -o errexit  # salir si cualquier comando falla

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Crear superusuario si no existe (usa variables de entorno de Render)
python manage.py shell -c "
from usuarios.models import Usuario
import os
correo    = os.environ.get('SUPERUSER_EMAIL')
password  = os.environ.get('SUPERUSER_PASSWORD')
nombres   = os.environ.get('SUPERUSER_NOMBRES', 'Admin')
apellidos = os.environ.get('SUPERUSER_APELLIDOS', 'Ruedo')
if correo and password and not Usuario.objects.filter(correo=correo).exists():
    Usuario.objects.create_superuser(correo=correo, password=password, nombres=nombres, apellidos=apellidos)
    print('Superusuario creado:', correo)
else:
    print('Superusuario ya existe o variables no definidas.')
"