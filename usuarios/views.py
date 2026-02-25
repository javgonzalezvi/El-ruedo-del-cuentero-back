"""
usuarios/views.py
"""

from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Usuario, EventoGuardado
from .serializers import (
    RegistroSerializer, PerfilSerializer,
    CambiarPasswordSerializer, EventoGuardadoSerializer,
    UsuarioPublicoSerializer,
)
from .permissions import EsPropietarioDePerfil, SoloAdmin


class RegistroView(generics.CreateAPIView):
    """POST /api/usuarios/registro/ — Crear cuenta nueva."""
    serializer_class   = RegistroSerializer
    permission_classes = [permissions.AllowAny]


class PerfilView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/usuarios/perfil/ — Ver y editar perfil propio."""
    serializer_class   = PerfilSerializer
    permission_classes = [permissions.IsAuthenticated, EsPropietarioDePerfil]

    def get_object(self):
        return self.request.user


class CambiarPasswordView(APIView):
    """POST /api/usuarios/cambiar-password/"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CambiarPasswordSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["password_nuevo"])
        request.user.save()
        return Response({"detail": "Contraseña actualizada correctamente."})


class ListaUsuariosView(generics.ListAPIView):
    """GET /api/usuarios/ — Solo Admins pueden listar todos los usuarios."""
    serializer_class   = UsuarioPublicoSerializer
    permission_classes = [SoloAdmin]
    queryset           = Usuario.objects.all()


class DetalleUsuarioView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/usuarios/<id>/ — Admin puede ver/editar cualquier usuario."""
    serializer_class   = PerfilSerializer
    permission_classes = [SoloAdmin]
    queryset           = Usuario.objects.all()


# ── Eventos guardados ──────────────────────────────────────────────────────

class EventosGuardadosView(generics.ListCreateAPIView):
    """GET/POST /api/usuarios/mis-eventos/ — Eventos guardados del usuario autenticado."""
    serializer_class   = EventoGuardadoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EventoGuardado.objects.filter(
            usuario=self.request.user
        ).select_related("evento")

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class EventoGuardadoDetalleView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PATCH/DELETE /api/usuarios/mis-eventos/<id>/"""
    serializer_class   = EventoGuardadoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EventoGuardado.objects.filter(usuario=self.request.user)