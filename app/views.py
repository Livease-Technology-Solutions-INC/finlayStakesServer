from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from .models import *
from .serializer import *

class BaseAPIView(APIView):
    model = None
    serializer_class = None
    permission_classes = []  # Add appropriate permission classes

    def get(self, request):
        instances = self.model.objects.all()
        serializer = self.serializer_class(instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomUserView(BaseAPIView):
    model = CustomUser
    serializer_class = CustomUserSerializer
    permission_classes = []  # Add appropriate permission classes

class PersonalDetailsView(BaseAPIView):
    model = PersonalDetails
    serializer_class = PersonalDetailsSerializer
    permission_classes = []  # Add appropriate permission classes

class CustomUserLoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)

class CustomUserRegistrationView(APIView):
    def post(self, request):
        serializer = CustomUserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomUserLogoutView(APIView):
    serializer_class = CustomUserLogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK)
