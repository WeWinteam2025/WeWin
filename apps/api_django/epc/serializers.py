from rest_framework import serializers
from .models import WorkOrder, RoofListing, Quote


class WorkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder
        fields = '__all__'


class RoofListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoofListing
        fields = '__all__'


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = '__all__'


