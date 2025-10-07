from django.db import models
from core.models import Organization


class CommunityEnergy(models.Model):
    organizacion = models.ForeignKey(Organization, on_delete=models.CASCADE)
    reglas = models.JSONField(default=dict, blank=True)
    nombre = models.CharField(max_length=255, default='Comunidad Energia')
    ciudad = models.CharField(max_length=100, default='', blank=True)
    barrio = models.CharField(max_length=100, default='', blank=True)
    historia = models.TextField(default='', blank=True)
    fotos_miembros = models.JSONField(default=list, blank=True)  # lista de URLs de rostros


class Voting(models.Model):
    ce = models.ForeignKey(CommunityEnergy, on_delete=models.CASCADE, related_name='votaciones')
    asunto = models.CharField(max_length=255)
    opciones = models.JSONField(default=list, blank=True)
    quorum = models.IntegerField(default=0)
    resultado = models.JSONField(default=dict, blank=True)





