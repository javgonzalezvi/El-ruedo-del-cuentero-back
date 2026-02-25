"""
usuarios/models.py

Modelo de usuario personalizado con sistema de roles.

Roles:
    USUARIO   → puede ver contenido, guardar eventos, tener preferencias
    CUENTERO  → puede crear/editar eventos, subir noticias y entrevistas
    ADMIN     → acceso total (incluyendo panel /admin/)

La diferenciación USUARIO vs CUENTERO se maneja con el campo `rol`
y con permisos personalizados en cada serializer/view.
"""

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UsuarioManager(BaseUserManager):
    """Manager personalizado que usa correo como identificador único."""

    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError("El correo es obligatorio.")
        correo = self.normalize_email(correo)
        extra_fields.setdefault("rol", Usuario.Rol.USUARIO)
        user = self.model(correo=correo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password=None, **extra_fields):
        extra_fields.setdefault("rol", Usuario.Rol.ADMIN)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(correo, password, **extra_fields)


def avatar_upload_path(instance, filename):
    return f"usuarios/{instance.pk}/avatar/{filename}"


class Usuario(AbstractBaseUser, PermissionsMixin):
    """
    Usuario personalizado del Ruedo del Cuentero.
    Reemplaza al User de Django con correo como username.
    """

    class Rol(models.TextChoices):
        USUARIO  = "USUARIO",  "Usuario"
        CUENTERO = "CUENTERO", "Cuentero"
        ADMIN    = "ADMIN",    "Administrador"

    # ── Identificación ──
    correo    = models.EmailField(unique=True, verbose_name="Correo electrónico")
    nombres   = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono  = models.CharField(max_length=20, blank=True)
    ciudad    = models.CharField(max_length=100, blank=True)

    # ── Rol ──
    rol = models.CharField(
        max_length=10,
        choices=Rol.choices,
        default=Rol.USUARIO,
        db_index=True,
    )

    # ── Perfil ──
    avatar = models.ImageField(
        upload_to=avatar_upload_path,
        null=True, blank=True,
        verbose_name="Foto de perfil",
    )

    # ── Preferencias de eventos (gustos) ──
    gustos = models.JSONField(
        default=list,
        blank=True,
        help_text='Lista de categorías de interés. Ej: ["CUENTO","FESTIVAL"]',
    )

    # ── Campos de sistema ──
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    fecha_union = models.DateTimeField(auto_now_add=True, verbose_name="Miembro desde")

    objects = UsuarioManager()

    USERNAME_FIELD  = "correo"
    REQUIRED_FIELDS = ["nombres", "apellidos"]

    class Meta:
        verbose_name        = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering            = ["-fecha_union"]

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.correo})"

    # ── Helpers de rol ──
    @property
    def es_cuentero(self):
        return self.rol in (self.Rol.CUENTERO, self.Rol.ADMIN)

    @property
    def es_admin(self):
        return self.rol == self.Rol.ADMIN

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"


class EventoGuardado(models.Model):
    """
    Relación M2M entre Usuario y Evento con metadatos adicionales.
    Registra si el usuario asistió o solo guardó el evento.
    """

    class Estado(models.TextChoices):
        GUARDADO = "GUARDADO", "Guardado"
        ASISTIDO = "ASISTIDO", "Asistido"

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="eventos_guardados",
    )
    evento = models.ForeignKey(
        "eventos.Evento",
        on_delete=models.CASCADE,
        related_name="guardado_por",
    )
    estado     = models.CharField(max_length=10, choices=Estado.choices, default=Estado.GUARDADO)
    fecha_alta = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("usuario", "evento")
        verbose_name        = "Evento guardado"
        verbose_name_plural = "Eventos guardados"

    def __str__(self):
        return f"{self.usuario} → {self.evento} [{self.estado}]"