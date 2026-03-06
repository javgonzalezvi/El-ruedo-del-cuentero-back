from rest_framework import serializers
from .models import Evento, Categoria, FechaEvento


class FechaEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = FechaEvento
        fields = ["id", "fecha", "nota"]


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Categoria
        fields = ["id", "nombre", "color", "slug"]


class EventoResumenSerializer(serializers.ModelSerializer):
    categoria     = CategoriaSerializer(read_only=True)
    imagen_final  = serializers.ReadOnlyField()
    video_final   = serializers.ReadOnlyField()
    fechas_adicionales = FechaEventoSerializer(many=True, read_only=True)

    class Meta:
        model  = Evento
        fields = [
            "id", "titulo", "descripcion", "categoria",
            "imagen_final", "imagen_url", "video_final", "video_url",
            "fecha", "lugar", "detalle_lugar", "ciudad",
            "recurrencia", "fechas_adicionales",
            "abierto", "destacado", "gratuito", "precio",
        ]


class EventoSerializer(serializers.ModelSerializer):
    categoria_id       = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), source="categoria",
        required=False, allow_null=True,
    )
    categoria          = CategoriaSerializer(read_only=True)
    imagen_final       = serializers.ReadOnlyField()
    video_final        = serializers.ReadOnlyField()
    fechas_adicionales = FechaEventoSerializer(many=True, read_only=True)

    class Meta:
        model  = Evento
        fields = [
            "id", "titulo", "descripcion",
            "categoria_id", "categoria",
            "imagen", "imagen_url", "imagen_final",
            "video", "video_url", "video_final",
            "fecha", "lugar", "detalle_lugar", "ciudad",
            "recurrencia", "fechas_adicionales",
            "abierto", "destacado", "gratuito", "precio",
            "creado_por", "creado_en",
        ]
        read_only_fields = ["creado_por", "creado_en", "imagen_final"]
