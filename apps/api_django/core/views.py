from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Organization, Actor, Project, Measurement, Contract, UserProfile
from .serializers import (
    OrganizationSerializer,
    ActorSerializer,
    ProjectSerializer,
    MeasurementSerializer,
    ContractSerializer,
    UserProfileSerializer,
)


class ReadPublicPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [ReadPublicPermission]


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [ReadPublicPermission]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # Lectura pública, escritura autenticada
    permission_classes = [ReadPublicPermission]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        estado = self.request.query_params.get('estado')
        only_active = self.request.query_params.get('active') or self.request.query_params.get('only_active')
        slug = self.request.query_params.get('slug')
        owner_user = self.request.query_params.get('owner_user')
        if estado:
            qs = qs.filter(estado__iexact=estado)
        elif only_active:
            qs = qs.filter(estado__in=['ACTIVO', 'ACTIVE', 'EN_CURSO', 'RUNNING'])
        if slug:
            qs = qs.filter(slug=slug)
        if owner_user:
            qs = qs.filter(owner__user__username=owner_user)
        limit = self.request.query_params.get('limit')
        if limit:
            try:
                qs = qs[: int(limit)]
            except Exception:
                pass
        return qs

    @action(detail=False, methods=['get'])
    def by_slug(self, request):
        slug = request.query_params.get('slug')
        if not slug:
            return Response({'error': 'slug requerido'}, status=400)
        try:
            p = Project.objects.get(slug=slug)
        except Project.DoesNotExist:
            return Response({'error': 'no encontrado'}, status=404)
        s = self.get_serializer(p)
        return Response(s.data)


class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    # Lectura pública; escritura autenticada
    permission_classes = [ReadPublicPermission]

    def get_queryset(self):
        qs = super().get_queryset()
        proyecto_id = self.request.query_params.get('proyecto')
        if proyecto_id:
            qs = qs.filter(proyecto_id=proyecto_id)
        return qs.order_by('-id')


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        current = self.request.query_params.get('current')
        if current:
            return qs.filter(user=self.request.user)
        return qs


