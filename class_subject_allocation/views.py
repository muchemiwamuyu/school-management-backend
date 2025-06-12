from django.shortcuts import render
from .serializers import ClassRegistrationSerializer, DepartmentsSerializer
from .models import ClassRegistration, Departments
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.


@api_view(['POST'])
def register_class(request):
    # Check if a class with the same unique fields already exists
    class_name = request.data.get('class_name')
    if class_name and ClassRegistration.objects.filter(class_name=class_name).exists():
        return Response(
            {"error": "A class with this name already exists."},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = ClassRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        response_data = serializer.data.copy()
        response_data['id'] = instance.id
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_classes(request):
    classes = ClassRegistration.objects.all()
    serializer = ClassRegistrationSerializer(classes, many=True)
    data = serializer.data
    # Ensure 'id' is included for each class
    for i, obj in enumerate(classes):
        if 'id' not in data[i]:
            data[i]['id'] = obj.id
    return Response(data, status=status.HTTP_200_OK)

@api_view(['PATCH'])
def update_class(request, class_id):
    try:
        class_instance = ClassRegistration.objects.get(id=class_id)
    except ClassRegistration.DoesNotExist:
        return Response({"error": "Class not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ClassRegistrationSerializer(class_instance, data=request.data, partial=True)
    if serializer.is_valid():
        updated_instance = serializer.save()
        response_data = serializer.data.copy()
        response_data['id'] = updated_instance.id
        return Response(response_data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_class(request, class_id):
    try:
        class_instance = ClassRegistration.objects.get(id=class_id)
    except ClassRegistration.DoesNotExist:
        return Response({"error": "Class not found."}, status=status.HTTP_404_NOT_FOUND)

    # Serialize class data before deletion
    serializer = ClassRegistrationSerializer(class_instance)
    class_data = serializer.data

    class_instance.delete()
    return Response(
        {
            "message": "Class deleted successfully.",
            "deleted_class": class_data
        },
        status=status.HTTP_204_NO_CONTENT
    )


# REMEMBER SUBJECTS FUNCTIONALITIES



@api_view(['POST'])
def departments_registration(request):
    # Check if a department with the same unique fields already exists
    department_name = request.data.get('department_name')
    if department_name and Departments.objects.filter(department_name=department_name).exists():
        return Response(
            {"error": "A department with this name already exists."},
            status=status.HTTP_400_BAD_REQUEST
        )
    serializer = DepartmentsSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        response_data = serializer.data.copy()
        response_data['id'] = instance.id
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)