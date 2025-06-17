from rest_framework import serializers
from .models import stakeHolders

class StakeHoldersSerializer(serializers.ModelSerializer):
    class Meta:
        model = stakeHolders
        fields = '__all__'

    def create(self, validated_data):
        return stakeHolders.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.message = validated_data.get('message', instance.message)

        instance.save()
        return instance