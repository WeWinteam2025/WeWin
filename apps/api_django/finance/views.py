from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Wallet, Movement, Settlement, Investment
from .serializers import WalletSerializer, MovementSerializer, SettlementSerializer, InvestmentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import Project, Measurement, Actor
from datetime import datetime


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

    @action(detail=False, methods=['get'])
    def portfolio_user(self, request):
        """Portafolio del usuario autenticado con cálculo de participación (%) y ganancias.
        - Percent = amount_cop / (potencia_kw * 3,000,000 COP)
        - Ingresos mensuales = sum(kwh_gen)*precio_cop_kw (COP)
        - Ganancia usuario = ingresos * percent * 0.9 (10% fee plataforma)
        """
        user = request.user
        try:
            investor = Actor.objects.filter(user=user, type='INVESTOR').first()
            if not investor:
                return Response({'projects': [], 'aggregate': {'months': [], 'user_income_12m_cop': [], 'income_12m_cop': [], 'total_user_income_12m_cop': 0}})
        except Exception:
            return Response({'projects': [], 'aggregate': {'months': [], 'user_income_12m_cop': [], 'income_12m_cop': [], 'total_user_income_12m_cop': 0}})

        invs = Investment.objects.filter(investor=investor).select_related('proyecto')
        # últimos 12 meses YYYY-MM
        today = datetime.utcnow()
        months_labels = []
        months_keys = []
        y = today.year
        m = today.month
        for _ in range(12):
            key = f"{y}-{m:02d}"
            months_keys.insert(0, key)
            months_labels.insert(0, ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'][m-1])
            m -= 1
            if m == 0:
                m = 12
                y -= 1

        agg_income = [0]*12
        agg_user_income = [0]*12
        projects = []
        for inv in invs:
            p = inv.proyecto
            if not p:
                continue
            try:
                kw = float(p.potencia_kw or 0)
            except Exception:
                kw = 0
            capex_cop = kw * 3000000.0  # aproximación
            amount_cop = float(inv.amount or 0)
            percent = 0.0
            if capex_cop > 0:
                percent = max(0.0, min(1.0, amount_cop / capex_cop))

            # obtener mediciones por periodo
            ms = Measurement.objects.filter(proyecto=p, periodo__in=months_keys).values('periodo','kwh_gen')
            by_key = { row['periodo']: float(row['kwh_gen']) for row in ms }
            price = float(p.precio_cop_kw or 0)
            proj_income = []
            user_income = []
            for idx, mk in enumerate(months_keys):
                gen = by_key.get(mk, 0.0)
                inc = gen * price
                uinc = inc * percent * 0.9  # fee 10%
                proj_income.append(inc)
                user_income.append(uinc)
                agg_income[idx] += inc
                agg_user_income[idx] += uinc

            projects.append({
                'id': p.id,
                'slug': p.slug or '',
                'ubicacion': p.ubicacion,
                'lat': float(p.lat) if p.lat is not None else None,
                'lng': float(p.lng) if p.lng is not None else None,
                'potencia_kw': float(p.potencia_kw or 0),
                'percent': round(percent*100, 2),
                'amount_cop': round(amount_cop, 2),
                'income_12m_cop': [round(x,2) for x in proj_income],
                'user_income_12m_cop': [round(x,2) for x in user_income],
                'user_income_total_cop': round(sum(user_income), 2),
            })

        return Response({
            'projects': projects,
            'aggregate': {
                'months': months_labels,
                'income_12m_cop': [round(x,2) for x in agg_income],
                'user_income_12m_cop': [round(x,2) for x in agg_user_income],
                'total_user_income_12m_cop': round(sum(agg_user_income), 2),
            }
        })


