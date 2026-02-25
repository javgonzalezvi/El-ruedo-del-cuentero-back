from django.contrib import admin
from .models import Noticia, BloqueContenido


class BloqueInline(admin.TabularInline):
    model  = BloqueContenido
    extra  = 1
    fields = ["tipo", "orden", "texto", "autor", "imagen", "src", "pie"]


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display    = ["titulo", "categoria", "autor", "publicada", "destacada", "fecha_publicacion"]
    list_filter     = ["categoria", "publicada", "destacada"]
    search_fields   = ["titulo", "resumen"]
    prepopulated_fields = {"slug": ("titulo",)}
    readonly_fields = ["creada_en", "actualizada"]
    raw_id_fields   = ["autor"]
    inlines         = [BloqueInline]