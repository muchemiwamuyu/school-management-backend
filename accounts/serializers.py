from rest_framework import serializers
from django.contrib.auth.models import User
from .models import RegisterSchoolStaff, School_Staff, DutyRoaster, Meeting
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

    def __str__(self):
        return super().__str__()
    
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
    

class DutyRoasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DutyRoaster
        fields = ['staff', 'duty', 'date', 'time']

    def create(self, validated_data):
        return DutyRoaster.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.staff = validated_data.get('staff', instance.staff)
        instance.duty = validated_data.get('duty', instance.duty)
        instance.date = validated_data.get('date', instance.date)
        instance.time = validated_data.get('time', instance.time)
        instance.save()
        return instance
    
class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ['title', 'agenda', 'description', 'status', 'created_at', 'updated_at']

    def create(self, validated_data):
        return Meeting.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.agenda = validated_data.get('agenda', instance.agenda)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

    


