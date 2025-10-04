from django.db import models
from core.models import Actor, Project


class EnergyOffer(models.Model):
    vendedor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='offers')
    proyecto = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    precio_ref = models.DecimalField(max_digits=12, decimal_places=4)
    capacidad_kw = models.DecimalField(max_digits=12, decimal_places=2)
    activo = models.BooleanField(default=True)


class EnergyDemand(models.Model):
    comprador = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='demands')
    perfil_carga = models.JSONField(default=dict, blank=True)
    precio_obj = models.DecimalField(max_digits=12, decimal_places=4)
    activo = models.BooleanField(default=True)




