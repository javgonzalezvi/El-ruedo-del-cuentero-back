"""eventos/views.py"""

from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Evento, Categoria
from .serializers import EventoSerializer, EventoResumenSerializer, CategoriaSerializer
from usuarios.permissions import EsCuenteroOAdmin, EsPropietarioOCuentero


class CategoriaViewSet(viewsets.ModelViewSet):
    """
    GET    /api/eventos/categorias/       → listar
    POST   /api/eventos/categorias/       → crear (solo Cuentero/Admin)
    GET    /api/eventos/categorias/<id>/  → detalle
    PUT    /api/eventos/categorias/<id>/  → editar
    DELETE /api/eventos/categorias/<id>/  → eliminar
    """
    queryset           = Categoria.objects.all()
    serializer_class   = CategoriaSerializer
    permission_classes = [EsCuenteroOAdmin]
    lookup_field       = "slug"


class EventoViewSet(viewsets.ModelViewSet):
    """
    GET    /api/eventos/           → listar (público)
    POST   /api/eventos/           → crear (solo Cuentero/Admin)
    GET    /api/eventos/<id>/      → detalle (público)
    PUT    /api/eventos/<id>/      → editar (solo creador o Admin)
    DELETE /api/eventos/<id>/      → eliminar (solo creador o Admin)

    Filtros disponibles:
        ?categoria=<slug>
        ?ciudad=<nombre>
        ?destacado=true
        ?abierto=true
        ?search=<texto>   → busca en título y descripción
        ?ordering=fecha   → ordenar por fecha
    """
    queryset = Evento.objects.select_related("categoria", "creado_por").all()
    filter_backends  = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["ciudad", "destacado", "abierto", "gratuito"]
    search_fields    = ["titulo", "descripcion", "lugar"]
    ordering_fields  = ["fecha", "creado_en"]
    ordering         = ["fecha"]

    def get_serializer_class(self):
        if self.action == "list":
            return EventoResumenSerializer
        return EventoSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        if self.action == "create":
            return [EsCuenteroOAdmin()]
        # update, partial_update, destroy
        return [permissions.IsAuthenticated(), EsPropietarioOCuentero()]

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)