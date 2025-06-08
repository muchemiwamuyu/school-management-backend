from rest_framework import serializers
from django.contrib.auth.models import User
from .models import RegisterSchoolStaff, School_Staff
from django.contrib.auth import authenticate

# Serializers define the API representation.

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validate_data):
        user = User.objects.create_user(
            username = validate_data['username'],
            email = validate_data['email'],
            password = validate_data['password']
        )
        return user
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        attrs['user'] = user
        return attrs
    

class RegisterSchoolStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterSchoolStaff
        exclude = ['created_by']  # Don't expect it from input

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)
    
class RegisterStaffSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = School_Staff
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        # Create the Django user
        user = User.objects.create_user(username=username, email=email, password=password)

        # Create the School_Staff profile
        staff = School_Staff.objects.create(user=user, **validated_data)
        return staff



class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = School_Staff
        fields = ['username', 'password']

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        attrs['user'] = user
        return attrs
    


