from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
from django.contrib.auth.password_validation import validate_password
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, Token


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser 
        fields = '__all__'
class PersonalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalDetails
        fields = '__all__'
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user): 
        token = super().get_token(user)
        
        token['name'] = user.personal_details.name
        token['email'] = user.email
        token['phone_number'] = str(user.phone_number)
        token['contact_number'] = str(user.personal_details.contact_number)
        token['nationality'] = user.personal_details.nationality
        return token
class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators = [validate_password]
    )
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
# class CustomUserLogoutSerializer(serializers.Serializer):
#     refresh = serializers.CharField()

#     def validate(self, data):
#         refresh = data.get('refresh')

#         if not refresh:
#             raise serializers.ValidationError('Refresh token is required.')

#         data['refresh'] = refresh
#         return data
    
# class CustomUserDetailView(RetrieveAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         return self.request.user