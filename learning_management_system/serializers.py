from rest_framework import serializers
from .models import Learning_Admin
from django.contrib.auth.models import User

# creating learning system serializers here...

class LearningSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Learning_Admin
        fields = '__all__'

    
        