"""
entrevistas/models.py

Entrevistas de audio a narradores orales.
Solo Cuenteros/Admins pueden crear y editar entrevistas.
"""

from django.db import models
from django.conf import settings


def audio_path(instance, filename):
    return f"entrevistas/{instance.pk}/audio/{filename}"

def imagen_entrevista_path(instance, filename):
    return f"entrevistas/{instance.pk}/imagen/{filename}"


class Entrevista(models.Model):

    class Categoria(models.TextChoices):
        MAESTROS        = "MAESTROS",        "Maestros"
        VOCES_NUEVAS    = "VOCES NUEVAS",    "Voces Nuevas"
        INTERNACIONAL   = "INTERNACIONAL",   "Internacional"
        EXPERIMENTALES  = "EXPERIMENTALES",  "Experimentales"

    # ── Información del entrevistado ──
    entrevistado = models.CharField(max_length=200, verbose_name="Nombre del entrevistado")
    rol          = models.CharField(max_length=200, verbose_name="Rol / descripción del entrevistado")

    # ── Contenido ──
    titulo            = models.CharField(max_length=300)
    slug              = models.SlugField(unique=True, max_length=320)
    resumen           = models.CharField(max_length=500)
    descripcion_larga = models.TextField(verbose_name="Descripción completa")

    # ── Imagen ──
    imagen     = models.ImageField(upload_to=imagen_entrevista_path, null=True, blank=True)
    imagen_url = models.URLField(blank=True, help_text="URL externa de imagen")

    # ── Audio ──
    audio_archivo = models.FileField(
        upload_to=audio_path,
        null=True, blank=True,
        verbose_name="Archivo de audio (MP3, WAV, OGG)",
    )
    audio_url = models.URLField(
        blank=True,
        help_text="URL externa de audio (SoundCloud, Spotify, etc.)",
    )
    duracion = models.CharField(
        max_length=10,
        blank=True,
        help_text='Duración en formato MM:SS. Ej: "38:24"',
    )

    # ── Clasificación ──
    categoria        = models.CharField(max_length=20, choices=Categoria.choices, default=Categoria.MAESTROS)
    categoria_color  = models.CharField(max_length=7, default="#C8572A")

    # ── Estado ──
    publicada = models.BooleanField(default=False)
    destacada = models.BooleanField(default=False)

    # ── Autoría (quién la subió) ──
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="entrevistas_creadas",
    )

    # ── Fechas ──
    fecha_publicacion = models.DateField(null=True, blank=True)
    creada_en         = models.DateTimeField(auto_now_add=True)
    actualizada       = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "Entrevista"
        verbose_name_plural = "Entrevistas"
        ordering            = ["-fecha_publicacion"]

    def __str__(self):
        return f"{self.titulo} — {self.entrevistado}"

    @property
    def imagen_final(self):
        if self.imagen:
            return self.imagen.url
        return self.imagen_url or None

    @property
    def audio_final(self):
        if self.audio_archivo:
            return self.audio_archivo.url
        return self.audio_url or None