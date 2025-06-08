from django.shortcuts import render
from .serializers import RegisterStudentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.


@api_view(['POST'])
def register_student(request):
    serializer = RegisterStudentSerializer(data=request.data)
    
    if serializer.is_valid():
        instance = serializer.save()
        # Generate access and refresh tokens for the registered student
        refresh = RefreshToken.for_user(instance)
        response_data = serializer.data.copy()
        response_data['id'] = instance.id
        response_data['access'] = str(refresh.access_token)
        response_data['refresh'] = str(refresh)
        # Return tokens in the response after registration
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Do a get request for the student registration
@api_view(['GET'])
def get_students(request):
    if request.method == 'GET':
        students = RegisterStudentSerializer.Meta.model.objects.all()
        serializer = RegisterStudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['PATCH'])
def update_student(request, student_id):
    try:
        student = RegisterStudentSerializer.Meta.model.objects.get(id=student_id)
    except RegisterStudentSerializer.Meta.model.DoesNotExist:
        return Response({"detail": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = RegisterStudentSerializer(student, data=request.data, partial=True)
    
    if serializer.is_valid():
        updated_student = serializer.save()
        return Response(RegisterStudentSerializer(updated_student).data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_student(request, student_id):
    try:
        student = RegisterStudentSerializer.Meta.model.objects.get(id=student_id)
    except RegisterStudentSerializer.Meta.model.DoesNotExist:
        return Response({"detail": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

    student.delete()
    return Response({"detail": "Student deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
#     staff_instance = serializer.save()
#     return Response(RegisterStudentSerializer(staff_instance).data, status=status.HTTP_201_CREATED)