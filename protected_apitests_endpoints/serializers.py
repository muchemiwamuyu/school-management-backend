from rest_framework import serializers
from django.contrib.auth.models import User
from .models import RegisterMainStaff
from django.contrib.auth import authenticate

# creating a user serializer

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class RegisterMainStaffSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = RegisterMainStaff
        fields = [
            'username', 'password',  # from User model
            'first_name', 'last_name', 'email', 'phone_number',
            'position', 'department'
        ]

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

        return RegisterMainStaff.objects.create(**validated_data)
    

class LoginStaffSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = RegisterMainStaff
        fields = ['username', 'password']

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError("Username and password are required.")

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid credentials.")

        return attrs
    
    
