"""
usuarios/urls_auth.py — Endpoints de autenticación JWT.

POST /api/auth/login/    → obtener access + refresh token
POST /api/auth/refresh/  → renovar access token con refresh
POST /api/auth/logout/   → invalidar refresh token (blacklist)
"""

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

urlpatterns = [
    path("login/",   TokenObtainPairView.as_view(),   name="auth-login"),
    path("refresh/", TokenRefreshView.as_view(),       name="auth-refresh"),
    path("logout/",  TokenBlacklistView.as_view(),     name="auth-logout"),
]