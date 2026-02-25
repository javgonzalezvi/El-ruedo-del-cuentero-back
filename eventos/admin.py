from django.contrib import admin
from .models import Evento, Categoria


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display  = ["nombre", "color", "slug"]
    prepopulated_fields = {"slug": ("nombre",)}


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display  = ["titulo", "categoria", "fecha", "ciudad", "abierto", "destacado", "creado_por"]
    list_filter   = ["categoria", "abierto", "destacado", "gratuito", "ciudad"]
    search_fields = ["titulo", "descripcion", "lugar"]
    ordering      = ["fecha"]
    readonly_fields = ["creado_en", "actualizado"]
    raw_id_fields   = ["creado_por"]