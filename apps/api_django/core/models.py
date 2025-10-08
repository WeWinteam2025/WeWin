from django.conf import settings
from django.db import models
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    avatar_url = models.URLField(blank=True, default='')
    avatar_file = models.ImageField(upload_to='avatars/', blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, default='')
    last_name = models.CharField(max_length=100, blank=True, default='')
    stakeholder_type = models.CharField(max_length=32, blank=True, default='')
    age = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, default='')
    country = models.CharField(max_length=100, blank=True, default='')
    email = models.EmailField(blank=True, default='')



class Organization(models.Model):
    name = models.CharField(max_length=255)
    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class Actor(models.Model):
    class ActorType(models.TextChoices):
        INVESTOR = 'INVESTOR'
        ROOF_OWNER = 'ROOF_OWNER'
        BUYER = 'BUYER'
        COMMUNITY = 'COMMUNITY'
        INSTALLER = 'INSTALLER'
        IMPORTER = 'IMPORTER'
        VENDOR = 'VENDOR'
        CONSULTANT = 'CONSULTANT'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='actors')
    type = models.CharField(max_length=32, choices=ActorType.choices)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)
    kyb_kyc = models.JSONField(default=dict, blank=True)

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.type} - {self.user_id}"


class Project(models.Model):
    class ProjectType(models.TextChoices):
        RESID = 'RESID'
        IND = 'IND'
        CE = 'CE'

    owner = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='projects')
    tipo = models.CharField(max_length=16, choices=ProjectType.choices)
    potencia_kw = models.DecimalField(max_digits=12, decimal_places=2)
    ubicacion = models.CharField(max_length=255)
    estado = models.CharField(max_length=64, default='INIT')
    image_url = models.URLField(blank=True, default='')
    slug = models.SlugField(unique=True, blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    descripcion = models.CharField(max_length=512, blank=True, default='')

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.tipo} {self.potencia_kw}kW"


class Measurement(models.Model):
    proyecto = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='measurements')
    periodo = models.CharField(max_length=16)
    kwh_gen = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    kwh_cons = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    kwh_exced = models.DecimalField(max_digits=14, decimal_places=2, default=0)


class Contract(models.Model):
    class ContractType(models.TextChoices):
        PPA = 'PPA'
        LEASING = 'LEASING'
        COMMUNITY = 'COMMUNITY'
        SERVICIO = 'SERVICIO'

    tipo = models.CharField(max_length=16, choices=ContractType.choices)
    partes = models.ManyToManyField(Actor, related_name='contracts')
    tarifa = models.DecimalField(max_digits=12, decimal_places=4)
    vigencia = models.CharField(max_length=64)
    proyecto = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    terms = models.JSONField(default=dict, blank=True)


