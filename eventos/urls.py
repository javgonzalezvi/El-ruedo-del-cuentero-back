"""eventos/urls.py"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventoViewSet, CategoriaViewSet

router = DefaultRouter()
router.register(r"categorias", CategoriaViewSet, basename="categoria")
router.register(r"",           EventoViewSet,    basename="evento")

urlpatterns = [path("", include(router.urls))]