from django.db import models
from core.models import Organization


class CommunityEnergy(models.Model):
    organizacion = models.ForeignKey(Organization, on_delete=models.CASCADE)
    reglas = models.JSONField(default=dict, blank=True)


class Voting(models.Model):
    ce = models.ForeignKey(CommunityEnergy, on_delete=models.CASCADE, related_name='votaciones')
    asunto = models.CharField(max_length=255)
    opciones = models.JSONField(default=list, blank=True)
    quorum = models.IntegerField(default=0)
    resultado = models.JSONField(default=dict, blank=True)





