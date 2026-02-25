"""noticias/serializers.py"""

from rest_framework import serializers
from usuarios.serializers import UsuarioPublicoSerializer
from .models import Noticia, BloqueContenido


class BloqueContenidoSerializer(serializers.ModelSerializer):
    src_final = serializers.CharField(read_only=True)

    class Meta:
        model  = BloqueContenido
        fields = ["id", "tipo", "orden", "texto", "autor", "imagen", "src", "src_final", "pie"]


class NoticiaResumenSerializer(serializers.ModelSerializer):
    """Vista compacta para listados."""
    autor              = UsuarioPublicoSerializer(read_only=True)
    imagen_portada_final = serializers.CharField(read_only=True)

    class Meta:
        model  = Noticia
        fields = [
            "id", "slug", "titulo", "resumen",
            "categoria", "categoria_color",
            "autor", "tiempo_lectura",
            "imagen_portada_final", "fecha_publicacion",
        ]


class NoticiaSerializer(serializers.ModelSerializer):
    """Serializer completo con bloques anidados."""
    autor              = UsuarioPublicoSerializer(read_only=True)
    bloques            = BloqueContenidoSerializer(many=True, read_only=True)
    imagen_portada_final = serializers.CharField(read_only=True)

    class Meta:
        model  = Noticia
        fields = [
            "id", "slug", "titulo", "resumen",
            "categoria", "categoria_color",
            "imagen_portada", "imagen_portada_url", "imagen_portada_final",
            "autor", "tiempo_lectura",
            "publicada", "destacada",
            "fecha_publicacion", "creada_en", "actualizada",
            "bloques",
        ]
        read_only_fields = ["id", "creada_en", "actualizada"]


class NoticiaWriteSerializer(serializers.ModelSerializer):
    """Para creación y edición (sin bloques anidados — se gestionan por separado)."""
    class Meta:
        model  = Noticia
        fields = [
            "titulo", "slug", "resumen",
            "categoria", "categoria_color",
            "imagen_portada", "imagen_portada_url",
            "tiempo_lectura", "publicada", "destacada",
            "fecha_publicacion",
        ]