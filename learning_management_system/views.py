from django.shortcuts import render
from .serializers import LearningSystemSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

# entry endpoint for the learning system
@api_view(['POST'])
def register_sys_admin(request):
    serializer = LearningSystemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


