from django.db import models
from core.models import Actor, Project


class WorkOrder(models.Model):
    instalador = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='ordenes')
    proyecto = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ordenes')
    estado = models.CharField(max_length=32, default='OPEN')
    hitos = models.JSONField(default=list, blank=True)


class RoofListing(models.Model):
    dueno = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='listings')
    ubicacion = models.CharField(max_length=255)
    sombras = models.CharField(max_length=255, blank=True, default='')
    fotos = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Quote(models.Model):
    listing = models.ForeignKey(RoofListing, on_delete=models.CASCADE, related_name='quotes')
    instalador = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='quotes')
    capex = models.DecimalField(max_digits=14, decimal_places=2)
    hitos = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=32, default='PENDING')


