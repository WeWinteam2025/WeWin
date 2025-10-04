from rest_framework import serializers
from .models import Product, B2BOrder


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class B2BOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = B2BOrder
        fields = '__all__'


