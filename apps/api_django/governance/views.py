from rest_framework import viewsets, permissions
from .models import CommunityEnergy, Voting
from .serializers import CommunityEnergySerializer, VotingSerializer


class CommunityEnergyViewSet(viewsets.ModelViewSet):
    queryset = CommunityEnergy.objects.all()
    serializer_class = CommunityEnergySerializer
    permission_classes = [permissions.IsAuthenticated]


class VotingViewSet(viewsets.ModelViewSet):
    queryset = Voting.objects.all()
    serializer_class = VotingSerializer
    permission_classes = [permissions.IsAuthenticated]





