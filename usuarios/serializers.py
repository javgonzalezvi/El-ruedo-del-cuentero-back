"""
usuarios/serializers.py
"""

from rest_framework import serializers
from .models import Usuario, EventoGuardado
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegistroSerializer(serializers.ModelSerializer):
    """Registro de un nuevo usuario (rol USUARIO por defecto)."""
    password  = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, label="Confirmar contraseña")

    class Meta:
        model  = Usuario
        fields = ["correo", "nombres", "apellidos", "telefono", "ciudad", "password", "password2"]

    def validate(self, data):
        if data["password"] != data.pop("password2"):
            raise serializers.ValidationError({"password2": "Las contraseñas no coinciden."})
        return data

    def create(self, validated_data):
        return Usuario.objects.create_user(**validated_data)


class UsuarioPublicoSerializer(serializers.ModelSerializer):
    """Vista pública mínima (para mostrar autor de noticias, etc.)."""
    nombre_completo = serializers.CharField(read_only=True)

    class Meta:
        model  = Usuario
        fields = ["id", "nombre_completo", "rol", "avatar", "ciudad"]


class PerfilSerializer(serializers.ModelSerializer):
    """
    Perfil completo del usuario autenticado.
    Permite editar campos personales y gustos.
    El campo `rol` solo puede cambiarlo un Admin.
    """
    nombre_completo = serializers.CharField(read_only=True)
    es_cuentero     = serializers.BooleanField(read_only=True)

    class Meta:
        model  = Usuario
        fields = [
            "id", "correo", "nombres", "apellidos",
            "telefono", "ciudad", "avatar",
            "gustos", "rol", "nombre_completo",
            "es_cuentero", "fecha_union",
        ]
        read_only_fields = ["id", "correo", "fecha_union"]

    def validate_rol(self, value):
        """Solo un Admin puede cambiar el rol de un usuario."""
        request = self.context.get("request")
        if request and not request.user.es_admin:
            # Si no es admin, ignorar cambio de rol
            return self.instance.rol if self.instance else value
        return value


class CambiarPasswordSerializer(serializers.Serializer):
    password_actual = serializers.CharField(write_only=True)
    password_nuevo  = serializers.CharField(write_only=True, min_length=8)
    password_nuevo2 = serializers.CharField(write_only=True, label="Confirmar nueva contraseña")

    def validate(self, data):
        if data["password_nuevo"] != data["password_nuevo2"]:
            raise serializers.ValidationError({"password_nuevo2": "Las contraseñas no coinciden."})
        return data

    def validate_password_actual(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("La contraseña actual no es correcta.")
        return value


class EventoGuardadoSerializer(serializers.ModelSerializer):
    from eventos.serializers import EventoResumenSerializer
    evento = EventoResumenSerializer(read_only=True)
    evento_id = serializers.PrimaryKeyRelatedField(
        queryset=__import__("eventos.models", fromlist=["Evento"]).Evento.objects.all(),
        source="evento",
        write_only=True,
    )

    class Meta:
        model  = EventoGuardado
        fields = ["id", "evento", "evento_id", "estado", "fecha_alta"]
        read_only_fields = ["id", "fecha_alta"]

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "correo"