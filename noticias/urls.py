"""noticias/urls.py"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers as nested_routers
from .views import NoticiaViewSet, BloqueContenidoViewSet

router = DefaultRouter()
router.register(r"", NoticiaViewSet, basename="noticia")

# Rutas anidadas: /api/noticias/<slug>/bloques/
bloques_router = nested_routers.NestedDefaultRouter(router, r"", lookup="noticia")
bloques_router.register(r"bloques", BloqueContenidoViewSet, basename="noticia-bloque")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(bloques_router.urls)),
]