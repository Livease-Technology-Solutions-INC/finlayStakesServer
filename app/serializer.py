from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class PersonalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalDetails
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    personal_details = PersonalDetailsSerializer()

    class Meta:
        model = get_user_model()  
        fields = '__all__'

    def create(self, validated_data):
        personal_details_data = validated_data.pop('personal_details')
        user = get_user_model().objects.create(**validated_data)
        PersonalDetails.objects.create(user=user, **personal_details_data)
        return user

class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password']

    def validate_email(self, value):
        if get_user_model().objects.filter(email=value).exists():
            raise serializers.ValidationError("Email address must be unique.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = get_user_model().objects.create_user(password=password, **validated_data)

        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return user, access_token

    
class CustomUserLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        # Include the access token in the response
        data['access'] = str(refresh.access_token)
        return data

class CustomUserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        refresh = data.get('refresh')

        if not refresh:
            raise serializers.ValidationError('Refresh token is required.')

        data['refresh'] = refresh
        return data
    
class CustomUserDetailView(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user