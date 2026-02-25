from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, EventoGuardado

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display  = ["correo", "nombres", "apellidos", "rol", "is_active", "fecha_union"]
    list_filter   = ["rol", "is_active", "ciudad"]
    search_fields = ["correo", "nombres", "apellidos"]
    ordering      = ["-fecha_union"]

    fieldsets = (
        (None,              {"fields": ("correo", "password")}),
        ("Información",     {"fields": ("nombres", "apellidos", "telefono", "ciudad", "avatar")}),
        ("Rol y acceso",    {"fields": ("rol", "gustos", "is_active", "is_staff", "is_superuser")}),
        ("Permisos",        {"fields": ("groups", "user_permissions")}),
        ("Fechas",          {"fields": ("last_login", "fecha_union")}),
    )
    readonly_fields   = ["fecha_union", "last_login"]
    add_fieldsets     = (
        (None, {
            "classes": ("wide",),
            "fields":  ("correo", "nombres", "apellidos", "rol", "password1", "password2"),
        }),
    )


@admin.register(EventoGuardado)
class EventoGuardadoAdmin(admin.ModelAdmin):
    list_display  = ["usuario", "evento", "estado", "fecha_alta"]
    list_filter   = ["estado"]
    search_fields = ["usuario__correo", "evento__titulo"]