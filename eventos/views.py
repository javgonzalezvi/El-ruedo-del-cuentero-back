from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Evento, Categoria, FechaEvento
from .serializers import EventoSerializer, EventoResumenSerializer, CategoriaSerializer, FechaEventoSerializer
from usuarios.permissions import EsCuenteroOAdmin


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset         = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.select_related("categoria").prefetch_related("fechas_adicionales").all()
    filter_backends  = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["ciudad", "destacado", "abierto", "categoria", "recurrencia"]
    search_fields    = ["titulo", "descripcion", "lugar"]
    ordering_fields  = ["fecha", "creado_en"]

    def get_serializer_class(self):
        if self.action == "list":
            return EventoResumenSerializer
        return EventoSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [EsCuenteroOAdmin()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        evento = serializer.save(creado_por=self.request.user)
        # Guardar fechas adicionales si vienen en el request
        fechas = self.request.data.get("fechas_adicionales", [])
        if isinstance(fechas, str):
            import json
            try:
                fechas = json.loads(fechas)
            except Exception:
                fechas = []
        for f in fechas:
            FechaEvento.objects.create(
                evento=evento,
                fecha=f.get("fecha"),
                nota=f.get("nota", ""),
            )


class FechaEventoViewSet(viewsets.ModelViewSet):
    serializer_class   = FechaEventoSerializer
    permission_classes = [EsCuenteroOAdmin]

    def get_queryset(self):
        return FechaEvento.objects.filter(evento_id=self.kwargs["evento_pk"])

    def perform_create(self, serializer):
        serializer.save(evento_id=self.kwargs["evento_pk"])