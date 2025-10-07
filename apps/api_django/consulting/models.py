from django.db import models
from core.models import Actor, Contract


class ConsultingService(models.Model):
    consultor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='servicios')
    categoria = models.CharField(max_length=128)
    precio_hora = models.DecimalField(max_digits=12, decimal_places=2)


class ConsultingPackage(models.Model):
    nombre = models.CharField(max_length=128)
    servicios = models.ManyToManyField(ConsultingService, related_name='paquetes')
    precio = models.DecimalField(max_digits=12, decimal_places=2)


class ConsultingContract(models.Model):
    contrato_base = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='consulting')
    paquete = models.ForeignKey(ConsultingPackage, on_delete=models.SET_NULL, null=True, blank=True)
    terms = models.JSONField(default=dict, blank=True)





