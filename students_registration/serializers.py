from rest_framework import serializers
from .models import RegisterStudents
from django.contrib.auth.models import User

class RegisterStudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = RegisterStudents
        fields = ['username', 'password', 'first_name', 'last_name', 'parents_email', 'parents_number', 'class_name', 'date_of_joining', 'date_of_birth']

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')

        # Create the user
        user = User.objects.create_user(username=username, password=password)
        validated_data['user'] = user

        # Optional: save name and email in User model too
        user.first_name = validated_data.get('first_name', '')
        user.last_name = validated_data.get('last_name', '')
        user.email = validated_data.get('email', '')
        user.save()

        return RegisterStudents.objects.create(**validated_data)