from rest_framework import serializers
from .models import EnergyOffer, EnergyDemand


class EnergyOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyOffer
        fields = '__all__'


class EnergyDemandSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyDemand
        fields = '__all__'





