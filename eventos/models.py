from django.db import models
from django.conf import settings
import uuid


def imagen_evento_path(instance, filename):
    ext = filename.rsplit(".", 1)[-1] if "." in filename else "jpg"
    return f"eventos/{uuid.uuid4().hex}.{ext}"


def video_evento_path(instance, filename):
    ext = filename.rsplit(".", 1)[-1] if "." in filename else "mp4"
    return f"eventos/videos/{uuid.uuid4().hex}.{ext}"


class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    color  = models.CharField(max_length=7, default="#C8572A")
    slug   = models.SlugField(unique=True)

    class Meta:
        verbose_name        = "Categoría"
        verbose_name_plural = "Categorías"
        ordering            = ["nombre"]

    def __str__(self):
        return self.nombre


class Evento(models.Model):

    RECURRENCIA_CHOICES = [
        ("ninguna", "Sin recurrencia"),
        ("semanal",  "Semanal"),
        ("mensual",  "Mensual"),
    ]

    titulo      = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    categoria   = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="eventos",
    )
    imagen     = models.ImageField(upload_to=imagen_evento_path, null=True, blank=True)
    imagen_url = models.URLField(blank=True)
    video      = models.FileField(
        upload_to=video_evento_path, null=True, blank=True,
        help_text="Archivo de video (sube a Cloudinary automáticamente)",
    )
    video_url  = models.URLField(blank=True, help_text="URL externa de video (YouTube, Vimeo, etc.)")

    fecha         = models.DateTimeField()
    lugar         = models.CharField(max_length=200)
    detalle_lugar = models.CharField(max_length=300, blank=True)
    ciudad        = models.CharField(max_length=100, default="Bogotá")

    recurrencia = models.CharField(
        max_length=10, choices=RECURRENCIA_CHOICES,
        default="ninguna", blank=True,
    )

    abierto   = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)
    gratuito  = models.BooleanField(default=True)
    precio    = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    creado_por  = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name="eventos_creados",
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
        if self.imagen:
            return self.imagen.url
        return self.imagen_url or None

    @property
    def video_final(self):
        if self.video:
            return self.video.url
        return self.video_url or None


class FechaEvento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="fechas_adicionales")
    fecha  = models.DateTimeField()
    nota   = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name        = "Fecha adicional"
        verbose_name_plural = "Fechas adicionales"
        ordering            = ["fecha"]

    def __str__(self):
        return f"{self.evento.titulo} — {self.fecha.strftime('%d/%m/%Y %H:%M')}"
    