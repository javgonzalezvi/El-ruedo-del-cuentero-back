from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers as nested_routers
from .views import EventoViewSet, CategoriaViewSet, FechaEventoViewSet

# Router principal solo para eventos
router = DefaultRouter()
router.register(r"", EventoViewSet, basename="evento")

# Router anidado para fechas: /api/eventos/<evento_pk>/fechas/
eventos_router = nested_routers.NestedDefaultRouter(router, r"", lookup="evento")
eventos_router.register(r"fechas", FechaEventoViewSet, basename="evento-fechas")

# Router separado para categorías
cat_router = DefaultRouter()
cat_router.register(r"", CategoriaViewSet, basename="categoria")

urlpatterns = [
    path("categorias/", include(cat_router.urls)),
    path("",            include(router.urls)),
    path("",            include(eventos_router.urls)),
]