from django.contrib import admin
from .models import Entrevista


@admin.register(Entrevista)
class EntrevistaAdmin(admin.ModelAdmin):
    list_display  = ["titulo", "entrevistado", "categoria", "publicada", "destacada", "fecha_publicacion"]
    list_filter   = ["categoria", "publicada", "destacada"]
    search_fields = ["titulo", "entrevistado", "resumen"]
    prepopulated_fields = {"slug": ("titulo",)}
    readonly_fields     = ["creada_en", "actualizada"]
    raw_id_fields       = ["creado_por"]