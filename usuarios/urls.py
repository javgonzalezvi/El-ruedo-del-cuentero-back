"""usuarios/urls.py — Endpoints de gestión de usuarios."""

from django.urls import path
from .views import (
    RegistroView, PerfilView, CambiarPasswordView,
    ListaUsuariosView, DetalleUsuarioView,
    EventosGuardadosView, EventoGuardadoDetalleView,
)

urlpatterns = [
    path("registro/",         RegistroView.as_view(),          name="usuario-registro"),
    path("perfil/",           PerfilView.as_view(),             name="usuario-perfil"),
    path("cambiar-password/", CambiarPasswordView.as_view(),    name="usuario-cambiar-password"),

    # Admin: listar y editar usuarios
    path("",                  ListaUsuariosView.as_view(),      name="usuario-lista"),
    path("<int:pk>/",         DetalleUsuarioView.as_view(),     name="usuario-detalle"),

    # Eventos guardados del usuario autenticado
    path("mis-eventos/",           EventosGuardadosView.as_view(),       name="mis-eventos"),
    path("mis-eventos/<int:pk>/",  EventoGuardadoDetalleView.as_view(),  name="mis-eventos-detalle"),
]