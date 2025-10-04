from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Wallet, Movement, Settlement, Investment
from .serializers import WalletSerializer, MovementSerializer, SettlementSerializer, InvestmentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import Project


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        try:
            wallet = Wallet.objects.get(id=pk)
        except Wallet.DoesNotExist:
            return Response({'error': 'wallet no encontrado'}, status=404)
        movs = Movement.objects.filter(wallet=wallet).order_by('-created_at')[:10]
        return Response({
            'wallet_id': wallet.id,
            'actor': wallet.actor_id,
            'saldo': wallet.saldo,
            'ultimos_movs': [
                {
                    'motivo': m.motivo,
                    'monto': float(m.monto),
                    'ref': m.ref,
                    'ts': m.created_at.isoformat(),
                } for m in movs
            ]
        })


class MovementViewSet(viewsets.ModelViewSet):
    queryset = Movement.objects.all()
    serializer_class = MovementSerializer
    permission_classes = [permissions.IsAuthenticated]


class SettlementViewSet(viewsets.ModelViewSet):
    queryset = Settlement.objects.all()
    serializer_class = SettlementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        contrato_id = self.request.query_params.get('contrato')
        if contrato_id:
            qs = qs.filter(contrato_id=contrato_id)
        return qs.order_by('-id')


class InvestmentViewSet(viewsets.ModelViewSet):
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def invest(self, request):
        investor_id = request.data.get('investor')
        proyecto_id = request.data.get('proyecto')
        amount = float(request.data.get('amount', 0))
        if amount < 100:  # ticket minimo demo
            return Response({'error': 'ticket mínimo 100'}, status=400)
        inv = Investment.objects.create(investor_id=investor_id, proyecto_id=proyecto_id, amount=amount)
        return Response({'id': inv.id})

    @action(detail=False, methods=['get'])
    def portfolio(self, request):
        investor_id = request.query_params.get('investor')
        qs = Investment.objects.filter(investor_id=investor_id)
        items = []
        for i in qs:
            # demo: rendimiento 8% anual prorrateado
            irr = float(i.expected_irr)
            items.append({'proyecto': i.proyecto_id, 'amount': float(i.amount), 'expected_irr': irr})
        return Response({'items': items})


