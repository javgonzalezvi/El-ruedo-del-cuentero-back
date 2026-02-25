"""entrevistas/serializers.py"""

from rest_framework import serializers
from usuarios.serializers import UsuarioPublicoSerializer
from .models import Entrevista


class EntrevistaResumenSerializer(serializers.ModelSerializer):
    imagen_final = serializers.CharField(read_only=True)

    class Meta:
        model  = Entrevista
        fields = [
            "id", "slug", "titulo", "entrevistado", "rol",
            "resumen", "categoria", "categoria_color",
            "imagen_final", "duracion", "fecha_publicacion",
        ]


class EntrevistaSerializer(serializers.ModelSerializer):
    creado_por   = UsuarioPublicoSerializer(read_only=True)
    imagen_final = serializers.CharField(read_only=True)
    audio_final  = serializers.CharField(read_only=True)

    class Meta:
        model  = Entrevista
        fields = [
            "id", "slug", "titulo", "entrevistado", "rol",
            "resumen", "descripcion_larga",
            "categoria", "categoria_color",
            "imagen", "imagen_url", "imagen_final",
            "audio_archivo", "audio_url", "audio_final", "duracion",
            "publicada", "destacada",
            "creado_por", "fecha_publicacion",
            "creada_en", "actualizada",
        ]
        read_only_fields = ["id", "creada_en", "actualizada"]