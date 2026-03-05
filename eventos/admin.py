from django.contrib import admin
from .models import Evento, Categoria, FechaEvento


class FechaEventoInline(admin.TabularInline):
    model  = FechaEvento
    extra  = 1
    fields = ["fecha", "nota"]


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display  = ["titulo", "fecha", "lugar", "recurrencia", "destacado", "abierto"]
    list_filter   = ["recurrencia", "destacado", "abierto", "gratuito", "categoria"]
    search_fields = ["titulo", "lugar"]
    inlines       = [FechaEventoInline]


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display  = ["nombre", "color", "slug"]
    prepopulated_fields = {"slug": ("nombre",)}