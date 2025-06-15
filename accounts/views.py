from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import UserSerializer, LoginSerializer, RegisterSchoolStaffSerializer, RegisterStaffSerializer, LoginSerializer, DutyRoasterSerializer, MeetingSerializer
from .models import RegisterSchoolStaff, DutyRoaster, Meeting, School_Staff
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import send_mail


User = get_user_model()


# Create your views here.
def index(request):
    return HttpResponse('Hello from accounts')

def ping(request):
    return JsonResponse({'message': 'pong from django'})


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    

    

@api_view(['POST'])
# @permission_classes([IsAuthenticated])  # Make sure the user is logged in
def register_school_staff(request):
    serializer = RegisterSchoolStaffSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        staff_instance = serializer.save()

        # Use the authenticated user directly
        # user = request.user

        # Generate JWT tokens
        # refresh = RefreshToken.for_user(user)
        # access_token = str(refresh.access_token)

        # link creation
        frontend_url = settings.FRONTEND_BASE_URL
        # redirect_link = f'{frontend_url}main-staff?token={access_token}'

        # Send link to the new staff's email
        # staff_email = staff_instance.email
        # send_mail(
        #     subject="Access Your School Staff Dashboard",
        #     message=f"Hi {staff_instance.first_name},\n\nYour account has been created. Click the link below to access the dashboard:\n\n{redirect_link}\n\nThis link contains your access token. Keep it safe.",
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     recipient_list=[staff_email],
        #     fail_silently=False
        # )

        return Response({
            "message": "School staff registered successfully.",
            "data": serializer.data,
            "token": {
                # "refresh": str(refresh),
                # "access": str(refresh.access_token),
                # "expiry": refresh.access_token['exp'],
            }
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# getting all staff
@api_view(['GET'])
def school_staff(request):
    teachers = RegisterSchoolStaff.objects.all()
    serializer = RegisterSchoolStaffSerializer(teachers, many=True)
    response = serializer.data

    return Response(response, status=status.HTTP_200_OK)
    

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def Registerstaff(request):
    serializer = RegisterStaffSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        staff_instance = serializer.save()
        return Response(RegisterStaffSerializer(staff_instance).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def LoginStaff(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "Login successful.",
                    "user": LoginSerializer(user).data,
                    "token": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "expiry": refresh.access_token['exp'],
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_dashboard(request):
    user = request.user

    try:
        staff = RegisterSchoolStaff.objects.get(created_by=user)
    except RegisterSchoolStaff.DoesNotExist:
        return Response({"error": "Staff record not found"}, status=404)

    # Duties assigned to the logged-in staff
    duties = DutyRoaster.objects.filter(staff=staff)

    # Optional: Filter meetings by department or other meaningful link
    meetings = Meeting.objects.filter(title__icontains=staff.first_name)  # TEMPORARY fallback

    dashboard_data = {
        "staff": {
            "first_name": staff.first_name,
            "last_name": staff.last_name,
            "position": staff.position,
            "department": staff.department,
        },
        "duties": [
            {
                "duty": d.duty,
                "date": d.date,
                "time": d.time,
            } for d in duties
        ],
        "meetings": [
            {
                "title": m.title,
                "agenda": m.agenda,
                "status": m.status,
                "created_at": m.created_at,
            } for m in meetings
        ]
    }

    return Response(dashboard_data, status=200)

@api_view(['GET'])
def list_users(request):
    users = User.objects.all().values('id', 'username', 'email')
    return Response(list(users))

    
@api_view(['POST'])
def duty_roaster(request):
    if request.method == 'POST':
        serializer = DutyRoasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def get_roaster(request):
    if request.method == 'GET':
        roasters = DutyRoaster.objects.all()
        serializer = DutyRoasterSerializer(roasters, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def create_meeting(request):
    if request.method == 'POST':
        serializer = MeetingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def get_meetings(request):
    if request.method == 'GET':
        meetings = Meeting.objects.all()
        serializer = MeetingSerializer(meetings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


