"""entrevistas/views.py"""

from rest_framework import viewsets, filters, permissions
from .models import Entrevista
from .serializers import EntrevistaSerializer, EntrevistaResumenSerializer
from usuarios.permissions import EsCuenteroOAdmin, EsPropietarioOCuentero


class EntrevistaViewSet(viewsets.ModelViewSet):
    """
    GET    /api/entrevistas/         → listar publicadas (público)
    POST   /api/entrevistas/         → crear (Cuentero/Admin)
    GET    /api/entrevistas/<slug>/  → detalle (público)
    PUT    /api/entrevistas/<slug>/  → editar (creador o Admin)
    DELETE /api/entrevistas/<slug>/  → eliminar (creador o Admin)

    Filtros: ?categoria=MAESTROS  ?destacada=true
    Búsqueda: ?search=vargas
    """
    lookup_field    = "slug"
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields   = ["titulo", "entrevistado", "resumen"]
    ordering_fields = ["fecha_publicacion", "creada_en"]
    ordering        = ["-fecha_publicacion"]

    def get_queryset(self):
        qs = Entrevista.objects.select_related("creado_por")
        if not self.request.user.is_authenticated or not self.request.user.es_cuentero:
            qs = qs.filter(publicada=True)
        categoria = self.request.query_params.get("categoria")
        destacada = self.request.query_params.get("destacada")
        if categoria:
            qs = qs.filter(categoria=categoria)
        if destacada:
            qs = qs.filter(destacada=destacada.lower() == "true")
        return qs

    def get_serializer_class(self):
        if self.action == "list":
            return EntrevistaResumenSerializer
        return EntrevistaSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        if self.action == "create":
            return [EsCuenteroOAdmin()]
        return [permissions.IsAuthenticated(), EsPropietarioOCuentero()]

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)