from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterUserSerializer, RegisterMainStaffSerializer, LoginStaffSerializer
from django.contrib.auth import authenticate
# Create your views here.

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Make sure the user is logged in
def register_main_staff(request):
    serializer = RegisterMainStaffSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        staff_instance = serializer.save()
        user = staff_instance.user  # this assumes your model has a user field

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Main staff registered successfully.",
            "data": serializer.data,
            "token": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def login_main_staff(request):
    serializer = LoginStaffSerializer(data=request.data)
    
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            return Response({
                "message": "Login successful."
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
