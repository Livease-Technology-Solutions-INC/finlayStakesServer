from rest_framework import serializers
from django.contrib.auth import get_user_model
from app.signals import create_token
from .models import *
from django.contrib.auth.password_validation import validate_password
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, Token


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class PersonalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalDetails
        fields = "__all__"


class IncomeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeDetails
        fields = "__all__"


class ExpenseDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseDetails
        fields = "__all__"


class AssetDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetDetails
        fields = "__all__"


class LiabilityDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiabilityDetails
        fields = "__all__"


class GoalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goals
        fields = "__all__"


class ExistingProvisionsDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExistingProvisionsDetails
        fields = "__all__"


class FinancialPlanningShortfallSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialPlanningShortfall
        fields = "__all__"


class ExistingPoliciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExistingPolicies
        fields = "__all__"


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["name"] = user.personal_details.name
        token["email"] = user.email
        token["phone_number"] = str(user.phone_number)
        token["phoneNumber"] = str(user.personal_details.phoneNumber)
        token["nationality"] = user.personal_details.nationality
        return token


class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    username = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ["email", "username", "password"]

    def create(self, validated_data):

        user = CustomUser.objects.create(
            email=validated_data["email"], username=validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.is_active = False
        user.save()

        create_token(sender=None, instance=user, created=True)

        return user


class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp_code = serializers.CharField(required=True)


# class CustomUserDetailView(RetrieveAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         return self.request.user
