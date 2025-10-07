from django.core.management.base import BaseCommand
from core.models import Contract, Measurement
from finance.models import Settlement, Wallet, Movement


class Command(BaseCommand):
    help = "Simulate monthly liquidation for all active PPA contracts"

    def handle(self, *args, **options):
        count = 0
        for ppa in Contract.objects.filter(tipo='PPA').exclude(proyecto=None):
            m = Measurement.objects.filter(proyecto=ppa.proyecto).order_by('-id').first()
            if not m:
                continue
            kwh = float(m.kwh_gen)
            tarifa = float(ppa.tarifa)
            bruto = kwh * tarifa
            fees = round(bruto * 0.05, 2)
            neto = round(bruto - fees, 2)
            Settlement.objects.get_or_create(
                contrato=ppa, periodo=m.periodo,
                defaults={'kwh': kwh, 'tarifa': tarifa, 'bruto': bruto, 'fees': fees, 'neto': neto}
            )
            partes = list(ppa.partes.all())
            if len(partes) >= 2:
                vendedor = partes[0]
                comprador = partes[1]
                v_wallet, _ = Wallet.objects.get_or_create(actor=vendedor)
                c_wallet, _ = Wallet.objects.get_or_create(actor=comprador)
                Movement.objects.create(wallet=v_wallet, motivo=f'Liquidación {m.periodo}', monto=neto, ref=f'PPA-{ppa.id}')
                Movement.objects.create(wallet=c_wallet, motivo=f'Pago {m.periodo}', monto=-neto, ref=f'PPA-{ppa.id}')
            count += 1
        self.stdout.write(self.style.SUCCESS(f'Liquidated {count} PPAs'))





