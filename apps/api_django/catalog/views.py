from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, B2BOrder
from .serializers import ProductSerializer, B2BOrderSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        marca = self.request.query_params.get('marca')
        potencia = self.request.query_params.get('potencia')
        stock = self.request.query_params.get('stock')
        if marca:
            qs = qs.filter(specs__marca__icontains=marca)
        if potencia:
            qs = qs.filter(specs__potencia__icontains=potencia)
        if stock:
            try:
                qs = qs.filter(stock__gte=int(stock))
            except Exception:
                pass
        return qs


class B2BOrderViewSet(viewsets.ModelViewSet):
    queryset = B2BOrder.objects.all()
    serializer_class = B2BOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def order(self, request):
        producto_id = request.data.get('producto')
        cantidad = int(request.data.get('cantidad', 1))
        comprador = request.data.get('comprador')
        if not comprador and request.user and request.user.is_authenticated:
            actor = getattr(request.user, 'actors', None)
            actor = actor.first() if actor else None
            if actor:
                comprador = actor.id
        try:
            p = Product.objects.get(id=producto_id)
        except Product.DoesNotExist:
            return Response({'error': 'producto no encontrado'}, status=404)
        if not comprador:
            return Response({'error': 'comprador requerido'}, status=400)
        total = float(p.precio) * cantidad
        order = B2BOrder.objects.create(comprador_id=comprador, producto=p, cantidad=cantidad, total=total, proforma={'producto': p.sku, 'total': total})
        return Response({'order_id': order.id, 'total': total})


