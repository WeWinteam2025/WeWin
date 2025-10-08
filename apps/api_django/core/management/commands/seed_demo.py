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
        # Imágenes: priorizamos techos (viviendas/empresas) con paneles solares
        # Usamos Unsplash Source para asegurar temática correcta
        residential_img = 'https://source.unsplash.com/1200x675/?house,rooftop,solar,panels'
        commercial_img = 'https://source.unsplash.com/1200x675/?building,roof,solar,panels'
        utility_img = 'https://source.unsplash.com/1200x675/?industrial,rooftop,solar,panels'

        def image_for(tipo:str, kw:float) -> str:
            try:
                kw = float(kw)
            except Exception:
                kw = 0
            if tipo == 'RESID' or kw <= 30:
                return residential_img
            if kw <= 220:
                return commercial_img
            return utility_img

        # Ensure three canonical projects exist with images; avoid duplicates
        p1 = Project.objects.filter(ubicacion='Zona Industrial').order_by('id').first()
        if not p1:
            p1 = Project.objects.create(owner=actors['ROOF_OWNER'], tipo='IND', potencia_kw=100, ubicacion='Zona Industrial', estado='ACTIVE', image_url=image_for('IND', 100), slug='zona-industrial')
        else:
            updated = False
            desired = image_for('IND', p1.potencia_kw)
            if (not p1.image_url) or ('source.unsplash.com' not in p1.image_url):
                p1.image_url = desired
                updated = True
            if p1.estado != 'ACTIVE':
                p1.estado = 'ACTIVE'
                updated = True
            if updated:
                p1.save()

        p2 = Project.objects.filter(ubicacion='Comunidad Energetica').order_by('id').first()
        if not p2:
            p2 = Project.objects.create(owner=actors['COMMUNITY'], tipo='CE', potencia_kw=500, ubicacion='Comunidad Energetica', estado='ACTIVE', image_url=image_for('CE', 500), slug='comunidad-energetica')
        else:
            updated = False
            desired = image_for('CE', p2.potencia_kw)
            if (not p2.image_url) or ('source.unsplash.com' not in p2.image_url):
                p2.image_url = desired
                updated = True
            if p2.estado != 'ACTIVE':
                p2.estado = 'ACTIVE'
                updated = True
            if updated:
                p2.save()

        p3 = Project.objects.filter(ubicacion='Residencial 12').order_by('id').first()
        if not p3:
            p3 = Project.objects.create(owner=actors['INVESTOR'], tipo='RESID', potencia_kw=12, ubicacion='Residencial 12', estado='PLANNING', image_url=image_for('RESID', 12), slug='residencial-12')
        else:
            desired = image_for('RESID', p3.potencia_kw)
            if (not p3.image_url) or ('source.unsplash.com' not in p3.image_url):
                p3.image_url = desired
                p3.save()
        # 18+ meses de mediciones para proyectos base
        def add_measure_series(proj, start_year=2024, start_month=4, months=18, base_kw=100):
            # Genera series mensuales con ligera variación, calcula excedentes
            y, m = start_year, start_month
            for i in range(months):
                periodo = f"{y}-{m:02d}"
                factor = 0.9 + ((i % 12)/120)  # leve tendencia
                gen = int(base_kw * 120 * factor)  # kWh mensual aproximado
                cons = int(gen * 0.78)
                exced = gen - cons
                obj, created = Measurement.objects.get_or_create(
                    proyecto=proj, periodo=periodo,
                    defaults={'kwh_gen': gen, 'kwh_cons': cons, 'kwh_exced': exced}
                )
                if not created:
                    # actualizar valores si ya existían
                    if obj.kwh_gen != gen or obj.kwh_cons != cons or obj.kwh_exced != exced:
                        obj.kwh_gen = gen
                        obj.kwh_cons = cons
                        obj.kwh_exced = exced
                        obj.save()
                m += 1
                if m > 12: m = 1; y += 1

        add_measure_series(p1, base_kw=100)
        add_measure_series(p2, base_kw=500)

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

        # ===== Catálogo ampliado (20+ productos de infraestructura solar) =====
        catalog_items = [
            # sku, precio USD, stock, specs
            ('PANEL-550W', 180, 500, {'tipo': 'panel', 'potencia': '550W', 'marca': 'JA Solar', 'cell': 'Mono PERC', 'garantia': '12/25 años'}),
            ('PANEL-450W', 145, 600, {'tipo': 'panel', 'potencia': '450W', 'marca': 'Canadian Solar', 'cell': 'Mono PERC'}),
            ('INV-3KW', 420, 60, {'tipo': 'inversor', 'potencia': '3kW', 'marca': 'Growatt', 'fase': 'Monofásico'}),
            ('INV-5KW', 620, 55, {'tipo': 'inversor', 'potencia': '5kW', 'marca': 'SMA', 'fase': 'Monofásico'}),
            ('INV-10KW', 980, 40, {'tipo': 'inversor', 'potencia': '10kW', 'marca': 'Huawei', 'fase': 'Trifásico'}),
            ('MICRO-600W', 115, 120, {'tipo': 'microinversor', 'potencia': '600W', 'marca': 'Hoymiles'}),
            ('BATT-5KWH-LFP', 1650, 30, {'tipo': 'batería', 'capacidad': '5kWh', 'quimica': 'LFP', 'marca': 'Pylontech'}),
            ('BATT-10KWH-LFP', 3150, 25, {'tipo': 'batería', 'capacidad': '10kWh', 'quimica': 'LFP', 'marca': 'BYD'}),
            ('MPPT-150V-70A', 390, 40, {'tipo': 'controlador', 'entrada': '150V', 'corriente': '70A', 'marca': 'Victron'}),
            ('ESTRUCT-TECHO-L', 45, 400, {'tipo': 'estructura', 'aplicacion': 'techo lámina', 'incluye': 'rieles+abrazaderas'}),
            ('ESTRUCT-TECHO-TEJA', 58, 300, {'tipo': 'estructura', 'aplicacion': 'teja arcilla', 'incluye': 'ganchos+rieles'}),
            ('CABLE-SOLAR-6MM', 0.95, 8000, {'tipo': 'cable', 'calibre': '6mm2', 'cert': 'TÜV'}),
            ('CABLE-SOLAR-4MM', 0.75, 12000, {'tipo': 'cable', 'calibre': '4mm2'}),
            ('MC4-PAR', 2.3, 4000, {'tipo': 'conector', 'modelo': 'MC4', 'par': True}),
            ('PROT-DC-1000V', 85, 70, {'tipo': 'protección', 'lado': 'DC', 'tension': '1000V'}),
            ('PROT-AC-400V', 79, 80, {'tipo': 'protección', 'lado': 'AC', 'tension': '400V'}),
            ('MEDIDOR-BIDIR', 260, 50, {'tipo': 'medidor', 'funcion': 'bidireccional', 'com': 'RS485'}),
            ('ESTAC-ON-GRID', 3500, 8, {'tipo': 'estacion', 'capacidad': '10kWp', 'incluye': ['inversor', 'paneles', 'estructura']}),
            ('KIT-RESID-3KW', 1850, 15, {'tipo': 'kit', 'potencia': '3kWp', 'uso': 'residencial'}),
            ('KIT-COM-20KW', 12500, 6, {'tipo': 'kit', 'potencia': '20kWp', 'uso': 'comercial'}),
            ('MONITOR-IOT', 140, 90, {'tipo': 'monitoreo', 'conectividad': 'WiFi/LTE'}),
        ]

        # Vendedores sintéticos con usuarios y clave demo
        seller_names = ['solarcol','enercom','andessun','colsol','megawatt']
        seller_users = []
        for name in seller_names:
            usr, _ = User.objects.get_or_create(username=name, defaults={'email': f'{name}@example.com'})
            if not usr.has_usable_password(): usr.set_password('demo'); usr.save()
            # Cada vendedor con su propia organización
            org_s, _ = Organization.objects.get_or_create(name=f"{name.upper()} Ltda")
            seller_actor, _ = Actor.objects.get_or_create(user=usr, type='VENDOR', defaults={'organization': org_s})
            seller_users.append(seller_actor)

        vendors = seller_users or [actors['VENDOR'], actors['IMPORTER'], actors['INSTALLER']]
        # Imagenes estables por tipo (evita 503 de Unsplash Source)
        stable_imgs = {
            'panel': 'https://images.unsplash.com/photo-1509395062183-67c5ad6faff9?q=80&w=800&auto=format',
            'inversor': 'https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=800&auto=format',
            'microinversor': 'https://images.unsplash.com/photo-1499951360447-b19be8fe80f5?q=80&w=800&auto=format',
            'batería': 'https://images.unsplash.com/photo-1581092332341-22f8c5f6f9b4?q=80&w=800&auto=format',
            'controlador': 'https://images.unsplash.com/photo-1518779578993-ec3579fee39f?q=80&w=800&auto=format',
            'estructura': 'https://images.unsplash.com/photo-1503104834685-7205e8607eb9?q=80&w=800&auto=format',
            'cable': 'https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=800&auto=format',
            'conector': 'https://images.unsplash.com/photo-1527430253228-e93688616381?q=80&w=800&auto=format',
            'protección': 'https://images.unsplash.com/photo-1558002038-1055907df827?q=80&w=800&auto=format',
            'medidor': 'https://images.unsplash.com/photo-1504384308090-c894fdcc538d?q=80&w=800&auto=format',
            'estacion': 'https://images.unsplash.com/photo-1469474968028-56623f02e42e?q=80&w=800&auto=format',
            'kit': 'https://images.unsplash.com/photo-1508514177221-188b1cf16b62?q=80&w=800&auto=format',
            'monitoreo': 'https://images.unsplash.com/photo-1527443224154-c4f2a4a2d140?q=80&w=800&auto=format',
        }

        for i, (sku, price, stock, specs) in enumerate(catalog_items):
            p, created = Product.objects.get_or_create(
                sku=sku,
                defaults={
                    'importador': actors['IMPORTER'],
                    'vendedor': vendors[i % len(vendors)],
                    'precio': price,
                    'stock': stock,
                    'specs': specs,
                    'image_url': stable_imgs.get(specs.get('tipo',''), 'https://images.unsplash.com/photo-1508514177221-188b1cf16b62?q=80&w=800&auto=format'),
                },
            )
            if not created:
                changed = False
                if (not getattr(p, 'image_url', '')) or ('source.unsplash.com' in p.image_url):
                    p.image_url = stable_imgs.get(specs.get('tipo',''), 'https://images.unsplash.com/photo-1508514177221-188b1cf16b62?q=80&w=800&auto=format')
                    changed = True
                if not p.vendedor:
                    p.vendedor = vendors[i % len(vendors)]
                    changed = True
                if changed:
                    p.save()

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

        # Governance CE + Voting (principal)
        ce, _ = CommunityEnergy.objects.get_or_create(organizacion=org, defaults={'reglas': {'quorum': 50}, 'nombre': 'CE We Win', 'ciudad': 'Bogotá', 'barrio': 'Chapinero', 'historia': 'Comunidad piloto enfocada en educación y medición transparente.', 'fotos_miembros': []})
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

        pdn, created_n = Project.objects.get_or_create(owner=roof2, tipo='IND', ubicacion='Bogotá Norte', defaults={'potencia_kw': 250, 'estado': 'ACTIVE', 'image_url': image_for('IND', 250), 'slug': 'bogota-norte', 'lat': 4.75, 'lng': -74.05, 'descripcion': 'Techo industrial con 250 kW para autoconsumo y venta de excedentes.'})
        if not created_n:
            desired = image_for('IND', pdn.potencia_kw)
            if (not pdn.image_url) or ('source.unsplash.com' not in pdn.image_url):
                pdn.image_url = desired
                pdn.save()
        pds, created_s = Project.objects.get_or_create(owner=roof2, tipo='IND', ubicacion='Medellín Sur', defaults={'potencia_kw': 180, 'estado': 'ACTIVE', 'image_url': image_for('IND', 180), 'slug': 'medellin-sur', 'lat': 6.20, 'lng': -75.58, 'descripcion': 'Cubierta comercial de 180 kW orientada a reducción de factura.'})
        if not created_s:
            desired = image_for('IND', pds.potencia_kw)
            if (not pds.image_url) or ('source.unsplash.com' not in pds.image_url):
                pds.image_url = desired
                pds.save()

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

        # Mediciones para proyectos de David (18+ meses)
        add_measure_series(pdn, base_kw=250)
        add_measure_series(pds, base_kw=180)

        # Inversión y número de paneles (aprox: 1 panel = 550W = 0.55 kW; costo 600 USD/kW)
        def calc_panels_and_capex(kw):
            panels = int(round(kw / 0.55))
            capex = int(round(kw * 600))  # USD
            return panels, capex
        for proj in [p1, p2, p3, pdn, pds]:
            panels, capex = calc_panels_and_capex(float(proj.potencia_kw))
            # Guardar en terms de un contrato dummy o metadata vía Wallet/Investment? Usamos Investment como proxy
            Investment.objects.get_or_create(investor=actors['INVESTOR'], proyecto=proj, defaults={'amount': capex, 'expected_irr': 12})

        # ===== 5 Comunidades Energéticas en diferentes ciudades =====
        faces = [
            'https://images.unsplash.com/photo-1544723795-3fb6469f5b39?q=80&w=400&auto=format',
            'https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=400&auto=format',
            'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?q=80&w=400&auto=format',
            'https://images.unsplash.com/photo-1527980965255-d3b416303d12?q=80&w=400&auto=format',
            'https://images.unsplash.com/photo-1524504388940-b1c1722653e1?q=80&w=400&auto=format',
        ]
        ce_data = [
            ('Comunidad Soledad Solar', 'Barranquilla', 'Soledad', '10 hogares se unieron para reducir su factura y vender excedentes al parque industrial cercano.'),
            ('Sol de Laureles', 'Medellín', 'Laureles', 'Vecinos organizaron compras conjuntas de paneles y ahora comercializan energía en horas de alta irradiación.'),
            ('Techos Verdes de Salitre', 'Bogotá', 'Salitre', 'Con apoyo del colegio local, instalaron monitoreo comunitario y educación para niños.'),
            ('Cali Brilla', 'Cali', 'Ciudad Jardín', 'Barrio residencial con techos amplios; optimizan autoconsumo y suben excedentes en PPA.'),
            ('Eje Solar Pereira', 'Pereira', 'Pinares', 'Comunidad piloto de 12 casas que migró a medición inteligente y venta a comercios.'),
        ]
        for i, (nombre, ciudad, barrio, historia) in enumerate(ce_data):
            CommunityEnergy.objects.get_or_create(
                nombre=nombre,
                ciudad=ciudad,
                barrio=barrio,
                defaults={
                    'organizacion': org,
                    'reglas': {'quorum': 50},
                    'historia': historia,
                    'fotos_miembros': faces + faces,  # al menos 10 rostros
                }
            )


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


