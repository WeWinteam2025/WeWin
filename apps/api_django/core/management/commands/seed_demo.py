from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Organization, Actor, Project, Contract, Measurement
from market.models import EnergyOffer, EnergyDemand
from finance.models import Wallet, Investment
from catalog.models import Product, B2BOrder
from epc.models import WorkOrder
from governance.models import CommunityEnergy, Voting
from consulting.models import ConsultingService, ConsultingPackage, ConsultingContract


class Command(BaseCommand):
    help = "Seed demo data: 8 actors, 1 CE-like org, buyer, installer, offers/demands"

    def handle(self, *args, **options):
        # Users
        u, _ = User.objects.get_or_create(username='demo', defaults={'is_staff': True})
        # Forzar credenciales demo/demo y activar usuario
        u.is_active = True
        u.set_password('demo')
        u.save()

        org, _ = Organization.objects.get_or_create(name='We Win CE')

        # Actors
        types = [
            'INVESTOR','ROOF_OWNER','BUYER','COMMUNITY','INSTALLER','IMPORTER','VENDOR','CONSULTANT'
        ]
        actors = {}
        for t in types:
            a, _ = Actor.objects.get_or_create(user=u, type=t, defaults={'organization': org})
            actors[t] = a

        # Extra users
        for name in ['instalador1', 'comprador1', 'vendedor1']:
            usr, _ = User.objects.get_or_create(username=name)
            if not usr.has_usable_password():
                usr.set_password('demo')
                usr.save()

        # Projects
        img1 = 'https://images.unsplash.com/photo-1581092795360-fd1ca04f0952?q=80&w=1200&auto=format'
        img2 = 'https://images.unsplash.com/photo-1509395176047-4a66953fd231?q=80&w=1200&auto=format'
        img3 = 'https://images.unsplash.com/photo-1509395062183-67c5ad6faff9?q=80&w=1200&auto=format'

        # Ensure three canonical projects exist with images; avoid duplicates
        p1 = Project.objects.filter(ubicacion='Zona Industrial').order_by('id').first()
        if not p1:
            p1 = Project.objects.create(owner=actors['ROOF_OWNER'], tipo='IND', potencia_kw=100, ubicacion='Zona Industrial', estado='ACTIVE', image_url=img1)
        else:
            updated = False
            if not p1.image_url:
                p1.image_url = img1
                updated = True
            if p1.estado != 'ACTIVE':
                p1.estado = 'ACTIVE'
                updated = True
            if updated:
                p1.save()

        p2 = Project.objects.filter(ubicacion='Comunidad Energetica').order_by('id').first()
        if not p2:
            p2 = Project.objects.create(owner=actors['COMMUNITY'], tipo='CE', potencia_kw=500, ubicacion='Comunidad Energetica', estado='ACTIVE', image_url=img2)
        else:
            updated = False
            if not p2.image_url:
                p2.image_url = img2
                updated = True
            if p2.estado != 'ACTIVE':
                p2.estado = 'ACTIVE'
                updated = True
            if updated:
                p2.save()

        p3 = Project.objects.filter(ubicacion='Residencial 12').order_by('id').first()
        if not p3:
            p3 = Project.objects.create(owner=actors['INVESTOR'], tipo='RESID', potencia_kw=12, ubicacion='Residencial 12', estado='PLANNING', image_url=img3)
        else:
            if not p3.image_url:
                p3.image_url = img3
                p3.save()
        # Measurements
        Measurement.objects.get_or_create(proyecto=p1, periodo='2025-09', defaults={'kwh_gen': 12450, 'kwh_cons': 9800, 'kwh_exced': 2650})
        Measurement.objects.get_or_create(proyecto=p2, periodo='2025-09', defaults={'kwh_gen': 73200, 'kwh_cons': 65000, 'kwh_exced': 8200})

        # Wallets
        for a in actors.values():
            Wallet.objects.get_or_create(actor=a, defaults={'saldo': 10000})

        # Offers/Demands
        EnergyOffer.objects.get_or_create(vendedor=actors['VENDOR'], proyecto=p1, precio_ref=0.25, capacidad_kw=50)
        EnergyOffer.objects.get_or_create(vendedor=actors['COMMUNITY'], proyecto=p2, precio_ref=0.20, capacidad_kw=120)
        # Ofertas extra
        EnergyOffer.objects.get_or_create(vendedor=actors['VENDOR'], proyecto=None, precio_ref=0.23, capacidad_kw=30)
        EnergyOffer.objects.get_or_create(vendedor=actors['COMMUNITY'], proyecto=None, precio_ref=0.19, capacidad_kw=80)
        EnergyDemand.objects.get_or_create(comprador=actors['BUYER'], precio_obj=0.22)
        EnergyDemand.objects.get_or_create(comprador=actors['COMMUNITY'], precio_obj=0.21)

        # Contract skeleton
        c, _ = Contract.objects.get_or_create(tipo='PPA', tarifa=0.21, vigencia='2025-2030')
        c.partes.set([actors['BUYER'].id, actors['VENDOR'].id])

        # Catalog products
        Product.objects.get_or_create(
            sku='INV-5KW',
            defaults={
                'importador': actors['IMPORTER'],
                'vendedor': actors['VENDOR'],
                'precio': 2200,
                'stock': 12,
                'specs': {'potencia': '5kW', 'marca': 'SunBest'},
            },
        )
        Product.objects.get_or_create(
            sku='PANEL-550W',
            defaults={
                'importador': actors['IMPORTER'],
                'vendedor': actors['VENDOR'],
                'precio': 180,
                'stock': 250,
                'specs': {'potencia': '550W', 'cell': 'Mono PERC'},
            },
        )

        # EPC work order
        WorkOrder.objects.get_or_create(
            instalador=actors['INSTALLER'], proyecto=p1,
            defaults={'estado': 'OPEN', 'hitos': [{'tarea': 'Visita técnica'}, {'tarea': 'Instalación'}]},
        )

        # Finance: one investment
        Investment.objects.get_or_create(investor=actors['INVESTOR'], proyecto=p1, defaults={'amount': 500, 'expected_irr': 12})

        # B2B Order: one order for installer
        prod = Product.objects.filter().first()
        if prod:
            B2BOrder.objects.get_or_create(comprador=actors['INSTALLER'], producto=prod, defaults={'cantidad': 2, 'total': prod.precio * 2, 'proforma': {'producto': prod.sku, 'cantidad': 2}})

        # Governance CE + Voting
        ce, _ = CommunityEnergy.objects.get_or_create(organizacion=org, defaults={'reglas': {'quorum': 50}})
        Voting.objects.get_or_create(ce=ce, asunto='Tarifa 2026', defaults={'opciones': ['Mantener', 'Subir 5%'], 'quorum': 50})

        # Consulting
        svc, _ = ConsultingService.objects.get_or_create(consultor=actors['CONSULTANT'], categoria='Diseño', defaults={'precio_hora': 80})
        pack, _ = ConsultingPackage.objects.get_or_create(nombre='Auditoría Energética', defaults={'precio': 1200})
        pack.servicios.add(svc)
        ConsultingContract.objects.get_or_create(contrato_base=c, paquete=pack)

        # ===== Custom user: davidgmarin@outlook.com como generador con 2 proyectos =====
        user_email = 'davidgmarin@outlook.com'
        u2, _ = User.objects.get_or_create(username=user_email.split('@')[0], defaults={'email': user_email, 'is_active': True})
        if not u2.has_usable_password():
            u2.set_password('demo')
            u2.save()
        org2, _ = Organization.objects.get_or_create(name='Generador David')
        vend2, _ = Actor.objects.get_or_create(user=u2, type='VENDOR', defaults={'organization': org2})
        roof2, _ = Actor.objects.get_or_create(user=u2, type='ROOF_OWNER', defaults={'organization': org2})

        imgN = 'https://images.unsplash.com/photo-1509395062183-67c5ad6faff9?q=80&w=1200&auto=format'
        imgS = 'https://images.unsplash.com/photo-1509395176047-4a66953fd231?q=80&w=1200&auto=format'
        pdn, _ = Project.objects.get_or_create(owner=roof2, tipo='IND', ubicacion='Bogotá Norte', defaults={'potencia_kw': 250, 'estado': 'ACTIVE', 'image_url': imgN})
        pds, _ = Project.objects.get_or_create(owner=roof2, tipo='IND', ubicacion='Medellín Sur', defaults={'potencia_kw': 180, 'estado': 'ACTIVE', 'image_url': imgS})

        # Dos compradores empresaA/empresaB
        empA, _ = User.objects.get_or_create(username='empresaA')
        if not empA.has_usable_password():
            empA.set_password('demo'); empA.save()
        empB, _ = User.objects.get_or_create(username='empresaB')
        if not empB.has_usable_password():
            empB.set_password('demo'); empB.save()
        buyerA, _ = Actor.objects.get_or_create(user=empA, type='BUYER')
        buyerB, _ = Actor.objects.get_or_create(user=empB, type='BUYER')

        # Ofertas de los dos proyectos
        EnergyOffer.objects.get_or_create(vendedor=vend2, proyecto=pdn, defaults={'precio_ref': 0.22, 'capacidad_kw': 90})
        EnergyOffer.objects.get_or_create(vendedor=vend2, proyecto=pds, defaults={'precio_ref': 0.21, 'capacidad_kw': 75})

        # Contratos PPA simulando venta a dos empresas
        cA, _ = Contract.objects.get_or_create(tipo='PPA', proyecto=pdn, tarifa=0.2150, vigencia='2025-2032')
        cA.partes.set([buyerA.id, vend2.id])
        cB, _ = Contract.objects.get_or_create(tipo='PPA', proyecto=pds, tarifa=0.2050, vigencia='2025-2031')
        cB.partes.set([buyerB.id, vend2.id])

        # ===== Catálogo de 12 empresas compradoras (reales en el mercado colombiano) =====
        companies = [
            'Grupo Éxito', 'Alpina', 'Postobón', 'Bavaria', 'Cementos Argos', 'Grupo Nutresa',
            'Bancolombia', 'Avianca', 'Carvajal', 'PepsiCo Colombia', 'Nestlé Colombia', 'Claro Colombia'
        ]
        for name in companies:
            uname = name.lower().replace(' ', '').replace('ó','o').replace('é','e').replace('á','a').replace('í','i').replace('ú','u').replace('ñ','n')
            ucmp, _ = User.objects.get_or_create(username=uname, defaults={'email': f'{uname}@example.com'})
            if not ucmp.has_usable_password():
                ucmp.set_password('demo'); ucmp.save()
            buyer, _ = Actor.objects.get_or_create(user=ucmp, type='BUYER')
            EnergyDemand.objects.get_or_create(comprador=buyer, defaults={'precio_obj': 0.22})

        self.stdout.write(self.style.SUCCESS('Seeded demo data'))


