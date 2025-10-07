from rest_framework import serializers
from .models import ConsultingService, ConsultingPackage, ConsultingContract


class ConsultingServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultingService
        fields = '__all__'


class ConsultingPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultingPackage
        fields = '__all__'


class ConsultingContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultingContract
        fields = '__all__'





