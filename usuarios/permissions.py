"""
usuarios/permissions.py

Permisos reutilizables en toda la API.
Se aplican con el decorador @permission_classes o en la clase ViewSet.
"""

from rest_framework.permissions import BasePermission, SAFE_METHODS

class EsCuenteroOAdmin(BasePermission):
    """
    Permite escritura solo a Cuenteros y Admins.
    Lectura libre para cualquier usuario autenticado o anónimo.
    """
    message = "Solo los Cuenteros pueden realizar esta acción."

    def has_permission(self, request, view):
        # GET, HEAD, OPTIONS → siempre permitidos
        if request.method in SAFE_METHODS:
            return True
        # Escritura → debe estar autenticado y ser cuentero/admin
        return (
            request.user
            and request.user.is_authenticated
            and request.user.es_cuentero
        )


class EsPropietarioOCuentero(BasePermission):
    """
    Permite modificar un objeto si:
        - El usuario es el creador del objeto (campo `creado_por`)
        - O el usuario es Admin
    Lectura siempre permitida.
    """
    message = "No tienes permiso para modificar este recurso."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.es_admin:
            return True
        creador = getattr(obj, "creado_por", None)
        return creador == request.user


class EsPropietarioDePerfil(BasePermission):
    """
    Solo el propio usuario puede editar su perfil.
    Admins pueden editar cualquier perfil.
    """
    message = "Solo puedes editar tu propio perfil."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.es_admin:
            return True
        return obj == request.user


class SoloAdmin(BasePermission):
    """Acceso exclusivo para administradores."""
    message = "Solo los administradores pueden acceder a este recurso."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.es_admin
        )