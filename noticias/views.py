"""noticias/views.py"""

from rest_framework import viewsets, filters, permissions
from .models import Noticia, BloqueContenido
from .serializers import (
    NoticiaSerializer, NoticiaResumenSerializer,
    NoticiaWriteSerializer, BloqueContenidoSerializer,
)
from usuarios.permissions import EsCuenteroOAdmin, EsPropietarioOCuentero


class NoticiaViewSet(viewsets.ModelViewSet):
    """
    GET    /api/noticias/          → listar publicadas (público)
    POST   /api/noticias/          → crear (Cuentero/Admin)
    GET    /api/noticias/<slug>/   → detalle (público)
    PUT    /api/noticias/<slug>/   → editar (autor o Admin)
    DELETE /api/noticias/<slug>/   → eliminar (autor o Admin)

    Filtros: ?categoria=CRÓNICA  ?destacada=true
    Búsqueda: ?search=cuenteria
    """
    lookup_field    = "slug"
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields   = ["titulo", "resumen"]
    ordering_fields = ["fecha_publicacion", "creada_en"]
    ordering        = ["-fecha_publicacion"]

    def get_queryset(self):
        qs = Noticia.objects.select_related("autor").prefetch_related("bloques")
        # Usuarios no autenticados solo ven noticias publicadas
        if not self.request.user.is_authenticated or not self.request.user.es_cuentero:
            qs = qs.filter(publicada=True)
        # Filtros opcionales
        categoria = self.request.query_params.get("categoria")
        destacada = self.request.query_params.get("destacada")
        if categoria:
            qs = qs.filter(categoria=categoria)
        if destacada:
            qs = qs.filter(destacada=destacada.lower() == "true")
        return qs

    def get_serializer_class(self):
        if self.action == "list":
            return NoticiaResumenSerializer
        if self.action in ["create", "update", "partial_update"]:
            return NoticiaWriteSerializer
        return NoticiaSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        if self.action == "create":
            return [EsCuenteroOAdmin()]
        return [permissions.IsAuthenticated(), EsPropietarioOCuentero()]

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)


class BloqueContenidoViewSet(viewsets.ModelViewSet):
    """
    Gestión de bloques de una noticia específica.
    GET    /api/noticias/<slug>/bloques/
    POST   /api/noticias/<slug>/bloques/
    PUT    /api/noticias/<slug>/bloques/<id>/
    DELETE /api/noticias/<slug>/bloques/<id>/
    """
    serializer_class = BloqueContenidoSerializer
    permission_classes = [EsCuenteroOAdmin]

    def get_queryset(self):
        return BloqueContenido.objects.filter(
            noticia__slug=self.kwargs["noticia_slug"]
        )

    def perform_create(self, serializer):
        noticia = Noticia.objects.get(slug=self.kwargs["noticia_slug"])
        serializer.save(noticia=noticia)