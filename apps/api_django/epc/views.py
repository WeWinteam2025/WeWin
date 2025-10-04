from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import WorkOrder, RoofListing, Quote
from .serializers import WorkOrderSerializer, RoofListingSerializer, QuoteSerializer
from finance.models import Wallet, Movement


class WorkOrderViewSet(viewsets.ModelViewSet):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def hito_complete(self, request, pk=None):
        order = self.get_object()
        idx = int(request.data.get('index', -1))
        if idx < 0:
            return Response({'error': 'index requerido'}, status=400)
        try:
            hito = order.hitos[idx]
        except Exception:
            return Response({'error': 'hito no existe'}, status=404)
        monto = float(hito.get('monto', 0))
        comprador = order.proyecto.owner
        iwallet, _ = Wallet.objects.get_or_create(actor=order.instalador)
        cw, _ = Wallet.objects.get_or_create(actor=comprador)
        Movement.objects.create(wallet=iwallet, motivo=f'Hito {idx} completado', monto=monto, ref=f'OT-{order.id}')
        Movement.objects.create(wallet=cw, motivo=f'Pago hito {idx}', monto=-monto, ref=f'OT-{order.id}')
        return Response({'ok': True})


class RoofListingViewSet(viewsets.ModelViewSet):
    queryset = RoofListing.objects.all()
    serializer_class = RoofListingSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuoteViewSet(viewsets.ModelViewSet):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def create_order(self, request):
        quote_id = request.data.get('quote_id')
        try:
            q = Quote.objects.get(id=quote_id)
        except Quote.DoesNotExist:
            return Response({'error': 'quote not found'}, status=404)
        from core.models import Project
        proyecto = Project.objects.create(owner=q.listing.dueno, tipo='IND', potencia_kw=10, ubicacion=q.listing.ubicacion, estado='PLANNING')
        order = WorkOrder.objects.create(instalador=q.instalador, proyecto=proyecto, estado='OPEN', hitos=q.hitos)
        q.status = 'ACCEPTED'
        q.save()
        return Response({'order_id': order.id})


