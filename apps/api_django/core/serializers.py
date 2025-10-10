from rest_framework import serializers
from .models import Organization, Actor, Project, Measurement, Contract, UserProfile


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    buyer_info = serializers.SerializerMethodField()
    seller_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = '__all__'
    
    def get_buyer_info(self, obj):
        """Obtener información del comprador de energía"""
        try:
            contract = obj.contract_set.filter(tipo='PPA').first()
            if contract and contract.partes.exists():
                buyer = contract.partes.filter(type='BUYER').first()
                if buyer:
                    return {
                        'username': buyer.user.username if buyer.user else '',
                        'organization': buyer.organization.name if buyer.organization else '',
                        'tarifa': contract.tarifa,
                        'vigencia': contract.vigencia
                    }
        except:
            pass
        return None
    
    def get_seller_info(self, obj):
        """Obtener información del vendedor de energía"""
        try:
            return {
                'username': obj.owner.user.username if obj.owner and obj.owner.user else '',
                'organization': obj.owner.organization.name if obj.owner and obj.owner.organization else '',
                'type': obj.owner.type if obj.owner else ''
            }
        except:
            pass
        return None


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = '__all__'


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

    def update(self, instance, validated_data):
        # Preserve values for syncing with auth_user after updating profile
        new_first = validated_data.get('first_name', instance.first_name)
        new_last = validated_data.get('last_name', instance.last_name)
        new_email = validated_data.get('email', instance.email)

        # Update profile fields first
        instance = super().update(instance, validated_data)

        # Sync basic fields to Django auth_user for consistency across the app
        user = getattr(instance, 'user', None)
        if user is not None:
            changed = False
            if new_first is not None and user.first_name != new_first:
                user.first_name = new_first
                changed = True
            if new_last is not None and user.last_name != new_last:
                user.last_name = new_last
                changed = True
            if new_email is not None and user.email != new_email:
                user.email = new_email
                changed = True
            if changed:
                # Save only the changed fields where possible
                try:
                    user.save()
                except Exception:
                    # If for some reason syncing fails, ignore to not break profile update
                    pass
        return instance


