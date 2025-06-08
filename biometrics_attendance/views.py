from django.shortcuts import render
from .serializers import FaceRegistrationSerializer
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
import numpy as np
import pickle
from .utils import cosine_similarity
from .models import FaceRegistration, Attendance
# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_face(request):
    # Ensure the user field is always the logged-in user
    data = request.data.copy()
    data['user'] = request.user.id  # set user to request.user

    serializer = FaceRegistrationSerializer(data=data)
    if serializer.is_valid():
        serializer.save()  # user is in data, serializer will use it
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def face_checkin(request):
    input_embedding = request.data.get('face_embedding')
    if not input_embedding:
        return Response({"error": "No face embedding provided."}, status=status.HTTP_400_BAD_REQUEST)

    # Convert input embedding to numpy array (assuming it's a list)
    try:
        input_embedding = np.array(input_embedding, dtype=float)
    except Exception:
        return Response({"error": "Invalid embedding format."}, status=status.HTTP_400_BAD_REQUEST)

    all_faces = FaceRegistration.objects.all()
    best_match_user = None
    best_similarity = -1
    SIMILARITY_THRESHOLD = 0.8  # tweak this based on your face model's accuracy

    for face_reg in all_faces:
        # Deserialize stored face data (assuming pickled numpy array)
        stored_embedding = pickle.loads(face_reg.face_data)

        similarity = cosine_similarity(input_embedding, stored_embedding)
        if similarity > best_similarity:
            best_similarity = similarity
            best_match_user = face_reg.user

    if best_similarity < SIMILARITY_THRESHOLD or best_match_user is None:
        return Response({
            "status": "failed",
            "message": "Face not recognized, please use fallback login"
        }, status=status.HTTP_401_UNAUTHORIZED)

    # Check if user already checked in today
    today = now().date()
    attendance_exists = Attendance.objects.filter(user=best_match_user, date=today).exists()

    if attendance_exists:
        return Response({
            "status": "failed",
            "message": "Already checked in today"
        }, status=status.HTTP_400_BAD_REQUEST)

    # Create attendance record
    Attendance.objects.create(user=best_match_user, date=today)

    return Response({
        "status": "success",
        "message": "Check-in successful",
        "user_id": best_match_user.id,
        "username": best_match_user.username
    }, status=status.HTTP_200_OK)

