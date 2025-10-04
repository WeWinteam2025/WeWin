from rest_framework import viewsets, permissions
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
    # Ahora todo acceso a proyectos requiere autenticación
    permission_classes = [permissions.IsAuthenticated]


class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = [permissions.IsAuthenticated]

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


