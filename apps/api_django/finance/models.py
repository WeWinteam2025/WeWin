from django.db import models
from core.models import Actor, Contract, Project


class Wallet(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='wallets')
    saldo = models.DecimalField(max_digits=14, decimal_places=2, default=0)


class Movement(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='movimientos')
    motivo = models.CharField(max_length=128)
    monto = models.DecimalField(max_digits=14, decimal_places=2)
    ref = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Settlement(models.Model):
    contrato = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='liquidaciones')
    periodo = models.CharField(max_length=16)
    kwh = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    tarifa = models.DecimalField(max_digits=12, decimal_places=4)
    bruto = models.DecimalField(max_digits=14, decimal_places=2)
    fees = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    neto = models.DecimalField(max_digits=14, decimal_places=2)


class Investment(models.Model):
    investor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='investments')
    proyecto = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='investments')
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    expected_irr = models.DecimalField(max_digits=5, decimal_places=2, default=10)
    created_at = models.DateTimeField(auto_now_add=True)


