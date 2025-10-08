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

    class Meta:
        model = Product
        fields = '__all__'


class B2BOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = B2BOrder
        fields = '__all__'


