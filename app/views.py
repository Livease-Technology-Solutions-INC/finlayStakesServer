from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render 
from rest_framework import generics
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

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class CustomUserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = ([AllowAny])
    serializer_class = CustomUserRegistrationSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def customUserDetail(request):
    if request.method == 'GET':
        response = f"Hey {request.user}, you are seeing a GET response"
        return Response({'response': response}, status=status.HTTP_200_OK)
    elif request.method == "POST":
        text = request.POST.get('text')
        response = f"Hey {request.user} your text is {text}"
        return Response({'response': response}, status=status.HTTP_200_OK)
    return Response({}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = "Hello buddy"
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)
# class CustomUserLogoutView(APIView):
#     serializer_class = CustomUserLogoutSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response(status=status.HTTP_200_OK)
