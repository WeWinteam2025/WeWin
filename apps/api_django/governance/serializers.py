from rest_framework import serializers
from .models import CommunityEnergy, Voting


class CommunityEnergySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityEnergy
        fields = '__all__'


class VotingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voting
        fields = '__all__'




