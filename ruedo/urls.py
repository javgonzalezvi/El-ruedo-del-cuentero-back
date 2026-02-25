"""
ruedo/urls.py

Enrutador principal. Cada app expone su propio router en urls.py.

Endpoints disponibles:
    /api/auth/          → login, refresh, logout (JWT)
    /api/usuarios/      → registro, perfil, gestión de usuarios
    /api/eventos/       → CRUD de eventos y categorías
    /api/noticias/      → CRUD de artículos y bloques de contenido
    /api/entrevistas/   → CRUD de entrevistas de audio
    /admin/             → panel de administración Django
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin de Django
    path("admin/", admin.site.urls),

    # Autenticación JWT
    path("api/auth/", include("usuarios.urls_auth")),

    # Apps
    path("api/usuarios/",    include("usuarios.urls")),
    path("api/eventos/",     include("eventos.urls")),
    path("api/noticias/",    include("noticias.urls")),
    path("api/entrevistas/", include("entrevistas.urls")),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)