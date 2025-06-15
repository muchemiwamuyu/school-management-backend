
# Create your views here.
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterStudentSerializer  # adjust if needed
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_welcome_email(user_email, full_name, student_id):
    link = f"http://localhost:5173/studentDetails/{student_id}"  # ← use 127.0.0.1 or your React dev port if needed

    html_content = render_to_string('emails/welcome.html', {
        'name': full_name,
        'email': user_email,
        'link': link,
    })

    email = EmailMessage(
        subject='Welcome to Our School Platform',
        body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user_email],
    )
    email.content_subtype = 'html'
    email.send()

# ✅ Student registration API view
@api_view(['POST'])
def register_student(request):
    serializer = RegisterStudentSerializer(data=request.data)

    if serializer.is_valid():
        instance = serializer.save()

        # Send HTML welcome email
        try:
            send_welcome_email(
                user_email=instance.parents_email,
                full_name=instance.first_name,
                student_id=instance.id
            )
        except Exception as e:
            print("❌ Email send failed:", e)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(instance)
        response_data = serializer.data.copy()
        response_data['id'] = instance.id
        response_data['access'] = str(refresh.access_token)
        response_data['refresh'] = str(refresh)

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