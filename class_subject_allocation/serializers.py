from rest_framework import serializers
from .models import ClassRegistration

class ClassRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRegistration
        fields = ['class_name', 'class_capacity', 'class_teacher']
    
    def create(self, validated_data):
        return ClassRegistration.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.class_name = validated_data.get('class_name', instance.class_name)
        instance.class_capacity = validated_data.get('class_capacity', instance.class_capacity)
        instance.class_teacher = validated_data.get('class_teacher', instance.class_teacher)
        instance.save()
        return instance