"""
noticias/models.py

Artículos de noticias con contenido estructurado en bloques
(igual que el diseño del frontend: párrafos, imágenes, citas, subtítulos).
Solo Cuenteros/Admins pueden crear y editar noticias.
"""

from django.db import models
from django.conf import settings


def imagen_noticia_path(instance, filename):
    return f"noticias/{instance.pk}/{filename}"

def imagen_bloque_path(instance, filename):
    return f"noticias/bloques/{instance.pk}/{filename}"


class Noticia(models.Model):

    class Categoria(models.TextChoices):
        CRONICA   = "CRÓNICA",   "Crónica"
        GUIA      = "GUÍA",      "Guía"
        EVENTO    = "EVENTO",    "Evento"
        REPORTAJE = "REPORTAJE", "Reportaje"

    # ── Cabecera ──
    titulo          = models.CharField(max_length=300)
    slug            = models.SlugField(unique=True, max_length=320)
    resumen         = models.TextField(max_length=500)
    imagen_portada  = models.ImageField(
        upload_to=imagen_noticia_path,
        null=True, blank=True,
    )
    imagen_portada_url = models.URLField(blank=True)

    # ── Clasificación ──
    categoria        = models.CharField(max_length=20, choices=Categoria.choices, default=Categoria.CRONICA)
    categoria_color  = models.CharField(max_length=7, default="#C8572A")

    # ── Autoría ──
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="noticias",
    )
    tiempo_lectura = models.PositiveSmallIntegerField(
        default=5,
        help_text="Tiempo estimado de lectura en minutos",
    )

    # ── Estado ──
    publicada   = models.BooleanField(default=False)
    destacada   = models.BooleanField(default=False)

    # ── Fechas ──
    fecha_publicacion = models.DateField(null=True, blank=True)
    creada_en         = models.DateTimeField(auto_now_add=True)
    actualizada       = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "Noticia"
        verbose_name_plural = "Noticias"
        ordering            = ["-fecha_publicacion"]

    def __str__(self):
        return self.titulo

    @property
    def imagen_portada_final(self):
        if self.imagen_portada:
            return self.imagen_portada.url
        return self.imagen_portada_url or None


class BloqueContenido(models.Model):
    """
    Bloque de contenido dentro de una noticia.
    Refleja exactamente la estructura del frontend:
        parrafo | subtitulo | imagen | cita
    """

    class Tipo(models.TextChoices):
        PARRAFO   = "parrafo",   "Párrafo"
        SUBTITULO = "subtitulo", "Subtítulo"
        IMAGEN    = "imagen",    "Imagen"
        CITA      = "cita",      "Cita"

    noticia = models.ForeignKey(
        Noticia,
        on_delete=models.CASCADE,
        related_name="bloques",
    )
    tipo  = models.CharField(max_length=15, choices=Tipo.choices)
    orden = models.PositiveSmallIntegerField(default=0)

    # Campos por tipo (se usa solo el relevante según `tipo`)
    texto  = models.TextField(blank=True)   # parrafo, subtitulo, cita.texto
    autor  = models.CharField(max_length=200, blank=True)  # cita.autor
    imagen = models.ImageField(upload_to=imagen_bloque_path, null=True, blank=True)
    src    = models.URLField(blank=True)    # imagen URL externa
    pie    = models.CharField(max_length=300, blank=True)  # imagen.pie de foto

    class Meta:
        ordering            = ["orden"]
        verbose_name        = "Bloque de contenido"
        verbose_name_plural = "Bloques de contenido"

    def __str__(self):
        return f"[{self.tipo}] Noticia {self.noticia_id} — orden {self.orden}"

    @property
    def src_final(self):
        if self.imagen:
            return self.imagen.url
        return self.src or None