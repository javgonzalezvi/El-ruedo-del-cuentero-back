"""entrevistas/urls.py"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EntrevistaViewSet

router = DefaultRouter()
router.register(r"", EntrevistaViewSet, basename="entrevista")

urlpatterns = [path("", include(router.urls))]