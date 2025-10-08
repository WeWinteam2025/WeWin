from rest_framework import serializers
from .models import Product, B2BOrder
from core.models import Actor


class ActorMiniSerializer(serializers.ModelSerializer):
    organization_name = serializers.SerializerMethodField()

    class Meta:
        model = Actor
        fields = ['id', 'type', 'organization_name']

    def get_organization_name(self, obj):
        return getattr(obj.organization, 'name', '')


class ProductSerializer(serializers.ModelSerializer):
    vendedor = ActorMiniSerializer(read_only=True)
    importador = ActorMiniSerializer(read_only=True)
    vendor_username = serializers.SerializerMethodField()
    vendor_org = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_vendor_username(self, obj):
        try:
            return getattr(obj.vendedor.user, 'username', '')
        except Exception:
            return ''

    def get_vendor_org(self, obj):
        try:
            return getattr(obj.vendedor.organization, 'name', '')
        except Exception:
            return ''


class B2BOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = B2BOrder
        fields = '__all__'


