"""eventos/serializers.py"""

from rest_framework import serializers
from .models import Evento, Categoria


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Categoria
        fields = ["id", "nombre", "color", "slug"]


class EventoResumenSerializer(serializers.ModelSerializer):
    """Vista compacta para listas y referencias externas (mis-eventos, etc.)."""
    categoria     = CategoriaSerializer(read_only=True)
    imagen_final  = serializers.CharField(read_only=True)

    class Meta:
        model  = Evento
        fields = [
            "id", "titulo", "categoria", "fecha",
            "lugar", "ciudad", "abierto", "destacado",
            "gratuito", "imagen_final",
        ]


class EventoSerializer(serializers.ModelSerializer):
    """Serializer completo para creación, edición y vista detallada."""
    categoria        = CategoriaSerializer(read_only=True)
    categoria_id     = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        source="categoria",
        write_only=True,
    )
    creado_por_nombre = serializers.SerializerMethodField()
    imagen_final      = serializers.CharField(read_only=True)

    class Meta:
        model  = Evento
        fields = [
            "id", "titulo", "descripcion",
            "categoria", "categoria_id",
            "imagen", "imagen_url", "imagen_final",
            "fecha", "lugar", "detalle_lugar", "ciudad",
            "abierto", "destacado", "gratuito", "precio",
            "creado_por_nombre", "creado_en", "actualizado",
        ]
        read_only_fields = ["id", "creado_en", "actualizado"]

    def get_creado_por_nombre(self, obj):
        if obj.creado_por:
            return obj.creado_por.nombre_completo
        return None