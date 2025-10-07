from rest_framework import viewsets, permissions
from .models import CommunityEnergy, Voting
from .serializers import CommunityEnergySerializer, VotingSerializer


class CommunityEnergyViewSet(viewsets.ModelViewSet):
    queryset = CommunityEnergy.objects.all()
    serializer_class = CommunityEnergySerializer
    # Lectura pública para listar comunidades
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class VotingViewSet(viewsets.ModelViewSet):
    queryset = Voting.objects.all()
    serializer_class = VotingSerializer
    permission_classes = [permissions.IsAuthenticated]





