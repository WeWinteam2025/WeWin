from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import EnergyOffer, EnergyDemand
from .serializers import EnergyOfferSerializer, EnergyDemandSerializer
from core.models import Contract, Project
from finance.models import Wallet, Movement, Settlement
from core.models import Measurement


class EnergyOfferViewSet(viewsets.ModelViewSet):
    queryset = EnergyOffer.objects.all()
    serializer_class = EnergyOfferSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'public']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def public(self, request):
        qs = EnergyOffer.objects.filter(activo=True)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        extra = {}
        user = self.request.user
        if user and user.is_authenticated and 'vendedor' not in serializer.validated_data:
            actor = getattr(user, 'actors', None)
            actor = actor.first() if actor else None
            if actor:
                extra['vendedor'] = actor
        serializer.save(**extra)


class EnergyDemandViewSet(viewsets.ModelViewSet):
    queryset = EnergyDemand.objects.all()
    serializer_class = EnergyDemandSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'public']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def public(self, request):
        qs = EnergyDemand.objects.filter(activo=True)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='ppa/create')
    def create_ppa(self, request):
        offer_id = request.data.get('offer_id')
        demand_id = request.data.get('demand_id')
        proyecto_id = request.data.get('proyecto_id')
        if not (offer_id and demand_id and proyecto_id):
            return Response({'error': 'offer_id, demand_id, proyecto_id requeridos'}, status=400)
        try:
            offer = EnergyOffer.objects.get(id=offer_id)
            demand = EnergyDemand.objects.get(id=demand_id)
            proyecto = Project.objects.get(id=proyecto_id)
        except Exception:
            return Response({'error': 'IDs inválidos'}, status=404)

        tarifa = float(offer.precio_ref)
        contrato = Contract.objects.create(
            tipo='PPA', tarifa=tarifa, vigencia='2025-2030', proyecto=proyecto, terms={'from_offer': offer.id, 'from_demand': demand.id}
        )
        contrato.partes.set([offer.vendedor_id, demand.comprador_id])
        offer.activo = False
        demand.activo = False
        offer.save(); demand.save()
        return Response({'ppa_id': contrato.id, 'tarifa': tarifa})

    @action(detail=True, methods=['get'], url_path='ppa/estado')
    def ppa_estado(self, request, pk=None):
        try:
            contrato = Contract.objects.get(id=pk, tipo='PPA')
        except Contract.DoesNotExist:
            return Response({'error': 'PPA no encontrado'}, status=404)
        m = Measurement.objects.filter(proyecto=contrato.proyecto).order_by('-id').first()
        kwh = float(m.kwh_gen) if m else 0.0
        tarifa = float(contrato.tarifa)
        bruto = kwh * tarifa
        fees = round(bruto * 0.05, 2)
        neto = round(bruto - fees, 2)
        return Response({'ppa_id': contrato.id, 'kwh': kwh, 'tarifa': tarifa, 'bruto': bruto, 'fees': fees, 'neto': neto})

    def perform_create(self, serializer):
        extra = {}
        user = self.request.user
        if user and user.is_authenticated and 'comprador' not in serializer.validated_data:
            actor = getattr(user, 'actors', None)
            actor = actor.first() if actor else None
            if actor:
                extra['comprador'] = actor
        serializer.save(**extra)


