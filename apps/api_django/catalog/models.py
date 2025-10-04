from django.db import models
from core.models import Actor


class Product(models.Model):
    importador = models.ForeignKey(Actor, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos_importados')
    vendedor = models.ForeignKey(Actor, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos_vendidos')
    sku = models.CharField(max_length=64, unique=True)
    specs = models.JSONField(default=dict, blank=True)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.IntegerField(default=0)


class B2BOrder(models.Model):
    comprador = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='orders')
    producto = models.ForeignKey(Product, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    total = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    proforma = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


