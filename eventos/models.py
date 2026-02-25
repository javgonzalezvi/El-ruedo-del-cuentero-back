"""
eventos/models.py

Modelos para la gestión de eventos de narración oral.
Solo los Cuenteros (y Admins) pueden crear/editar eventos.
"""

from django.db import models
from django.conf import settings


def imagen_evento_path(instance, filename):
    return f"eventos/{instance.pk}/{filename}"


class Categoria(models.Model):
    """Categorías de eventos: CUENTO, FESTIVAL, TALLER, RUEDO, etc."""
    nombre = models.CharField(max_length=50, unique=True)
    color  = models.CharField(max_length=7, default="#C8572A", help_text="Color HEX, ej: #C8572A")
    slug   = models.SlugField(unique=True)

    class Meta:
        verbose_name        = "Categoría"
        verbose_name_plural = "Categorías"
        ordering            = ["nombre"]

    def __str__(self):
        return self.nombre


class Evento(models.Model):
    """
    Evento de narración oral.
    Creado y gestionado por Cuenteros/Admins.
    """

    # ── Información básica ──
    titulo      = models.CharField(max_length=200)
    descripcion = models.TextField()
    categoria   = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        related_name="eventos",
    )
    imagen = models.ImageField(
        upload_to=imagen_evento_path,
        null=True, blank=True,
        verbose_name="Imagen del evento",
    )
    imagen_url = models.URLField(
        blank=True,
        help_text="URL externa de imagen (alternativa a subir archivo)",
    )

    # ── Fecha y lugar ──
    fecha        = models.DateTimeField(verbose_name="Fecha y hora del evento")
    lugar        = models.CharField(max_length=200, verbose_name="Nombre del lugar")
    detalle_lugar = models.CharField(
        max_length=300, blank=True,
        verbose_name="Dirección o detalle del lugar",
    )
    ciudad = models.CharField(max_length=100, default="Bogotá")

    # ── Estado ──
    abierto    = models.BooleanField(default=True, verbose_name="Inscripciones abiertas")
    destacado  = models.BooleanField(default=False, verbose_name="Evento destacado")
    gratuito   = models.BooleanField(default=True)
    precio     = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True,
        help_text="Precio en COP si no es gratuito",
    )

    # ── Metadata ──
    creado_por  = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="eventos_creados",
        verbose_name="Creado por",
    )
    creado_en   = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "Evento"
        verbose_name_plural = "Eventos"
        ordering            = ["fecha"]

    def __str__(self):
        return f"{self.titulo} — {self.fecha.strftime('%d/%m/%Y')}"

    @property
    def imagen_final(self):
        """Devuelve la URL de imagen, priorizando el archivo subido."""
        if self.imagen:
            return self.imagen.url
        return self.imagen_url or None