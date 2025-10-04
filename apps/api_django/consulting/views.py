from rest_framework import viewsets, permissions
from .models import ConsultingService, ConsultingPackage, ConsultingContract
from .serializers import ConsultingServiceSerializer, ConsultingPackageSerializer, ConsultingContractSerializer


class ConsultingServiceViewSet(viewsets.ModelViewSet):
    queryset = ConsultingService.objects.all()
    serializer_class = ConsultingServiceSerializer
    permission_classes = [permissions.IsAuthenticated]


class ConsultingPackageViewSet(viewsets.ModelViewSet):
    queryset = ConsultingPackage.objects.all()
    serializer_class = ConsultingPackageSerializer
    permission_classes = [permissions.IsAuthenticated]


class ConsultingContractViewSet(viewsets.ModelViewSet):
    queryset = ConsultingContract.objects.all()
    serializer_class = ConsultingContractSerializer
    permission_classes = [permissions.IsAuthenticated]




