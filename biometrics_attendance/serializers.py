from rest_framework import serializers
from .models import FaceRegistration
import base64
from rest_framework import serializers


class FaceRegistrationSerializer(serializers.ModelSerializer):
    # Override face_data to accept base64 encoded string
    face_data = serializers.CharField(write_only=True)

    class Meta:
        model = FaceRegistration
        fields = ['name', 'face_data', 'registered_at']
        read_only_fields = ['registered_at']

    def validate_face_data(self, value):
        try:
            # Decode base64 string to bytes
            decoded_data = base64.b64decode(value)
        except Exception:
            raise serializers.ValidationError("Invalid base64-encoded data for face_data.")
        return decoded_data

    def create(self, validated_data):
        # Extract face_data bytes from validated_data
        face_data_bytes = validated_data.pop('face_data')
        user = validated_data.get('user')

        # Update existing or create new face registration for the user
        instance, created = FaceRegistration.objects.update_or_create(
            user=user,
            defaults={'face_data': face_data_bytes}
        )
        return instance

