from rest_framework import serializers
from .models import ClassRegistration, Departments

class ClassRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRegistration
        fields = '__all__'
    
    def create(self, validated_data):
        return ClassRegistration.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.class_name = validated_data.get('class_name', instance.class_name)
        instance.class_capacity = validated_data.get('class_capacity', instance.class_capacity)
        instance.class_teacher = validated_data.get('class_teacher', instance.class_teacher)

        instance.save()
        return instance
    
class DepartmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = '__all__'
            
    def create(self, validated_data):
        return Departments.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.department_name = validated_data.get('department_name', instance.department_name)
        instance.department_role = validated_data.get('department_role', instance.department_role)
        instance.dean = validated_data.get('dean', instance.dean)

        instance.save()
        return instance