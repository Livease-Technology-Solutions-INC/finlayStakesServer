from django.http import Http404, JsonResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from .models import *
from .serializer import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.generics import ListCreateAPIView


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


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        return obj.user == request.user


class CustomUserView(BaseAPIView):
    model = CustomUser
    serializer_class = CustomUserSerializer
    permission_classes = []


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class CustomUserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CustomUserRegistrationSerializer


class VerifyEmailView(generics.CreateAPIView):
    serializer_class = OTPVerificationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        otp_code = serializer.validated_data.get("otp_code")

        # Get the user associated with the provided email
        user = get_object_or_404(CustomUser, email=email)

        # Check if the user has a corresponding OTP token
        otp_token = OtpToken.objects.filter(user=user).last()
        if otp_token:
            # Verify if the OTP token matches
            if otp_token.otp_code == otp_code:
                # Verify if the OTP token is still valid
                if otp_token.otp_expires_at > timezone.now():
                    # Activate the user account
                    user.is_active = True
                    user.save()
                    # Delete the OTP token as it's no longer needed
                    otp_token.delete()
                    return Response(
                        {"detail": "Email verified successfully!"},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"detail": "OTP token has expired. Please request a new one."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"detail": "Invalid OTP code."}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"detail": "No OTP token found for this email address."},
                status=status.HTTP_404_NOT_FOUND,
            )


class ResendOTPView(generics.CreateAPIView):
    def get_serializer(self, *args, **kwargs):
        """
        Overriding the get_serializer method to prevent serializer instantiation
        """
        return None

    def post(self, request, *args, **kwargs):
        user_email = kwargs.get("email")  
        if get_user_model().objects.filter(email=user_email).exists():
            user = get_user_model().objects.get(email=user_email)

            # Delete any existing OTP tokens for the user
            OtpToken.objects.filter(user=user).delete()

            # Create a new OTP token for the user
            otp = OtpToken.objects.create(
                user=user,
                otp_expires_at=timezone.now() + timezone.timedelta(minutes=5),
            )

            # Trigger sending email via signal (if implemented)
            # Assuming the signal is responsible for sending the OTP email

            return Response(
                {"detail": "OTP resent successfully!"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )


@api_view(["GET", "POST"])
def PersonalDetailsView(request, id):
    try:
        personaldetails = PersonalDetails.objects.get(id=id)
    except PersonalDetails.DoesNotExist:
        return Response(
            {"error": "Personal details not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        serializer = PersonalDetailsSerializer(personaldetails)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = PersonalDetailsSerializer(
            instance=personaldetails, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def IncomeDetailsView(request, id):
    try:
        incomedetails = IncomeDetails.objects.get(id=id)
    except IncomeDetails.DoesNotExist:
        return Response(
            {"error": "income details not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        serializer = IncomeDetailsSerializer(incomedetails)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = IncomeDetailsSerializer(instance=incomedetails, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def ExpenseDetailsView(request, id):
    try:
        expensedetails = ExpenseDetails.objects.get(id=id)
    except ExpenseDetails.DoesNotExist:
        return Response(
            {"error": "expense details not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        serializer = ExpenseDetailsSerializer(expensedetails)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = ExpenseDetailsSerializer(
            instance=expensedetails, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def AssetDetailsView(request, id):
    try:
        assetdetails = AssetDetails.objects.get(id=id)
    except AssetDetails.DoesNotExist:
        return Response(
            {"error": "asset details not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        serializer = AssetDetailsSerializer(assetdetails)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = AssetDetailsSerializer(instance=assetdetails, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def LiabilityDetailsView(request, id):
    try:
        liabilitydetails = LiabilityDetails.objects.get(id=id)
    except LiabilityDetails.DoesNotExist:
        return Response(
            {"error": "liability details not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        serializer = LiabilityDetailsSerializer(liabilitydetails)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = LiabilityDetailsSerializer(
            instance=liabilitydetails, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def GoalsView(request, id):
    try:
        goals = Goals.objects.get(id=id)
    except Goals.DoesNotExist:
        return Response(
            {"error": "Goal details not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        serializer = GoalsSerializer(goals)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = GoalsSerializer(instance=goals, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def ExistingProvisionsDetailsView(request, id):
    try:
        existingProvisionsDetails = ExistingProvisionsDetails.objects.get(id=id)
    except ExistingProvisionsDetails.DoesNotExist:
        return Response(
            {"error": "ExistingProvisions details not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        serializer = ExistingProvisionsDetailsSerializer(existingProvisionsDetails)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = ExistingProvisionsDetailsSerializer(
            instance=existingProvisionsDetails, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def FinancialPlanningShortfallView(request, id):
    try:
        financialPlanningShortfall = FinancialPlanningShortfall.objects.get(id=id)
    except FinancialPlanningShortfall.DoesNotExist:
        return Response(
            {"error": "FinancialPlanningShortfall details not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        serializer = FinancialPlanningShortfallSerializer(financialPlanningShortfall)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = FinancialPlanningShortfallSerializer(
            instance=financialPlanningShortfall, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def ExistingPoliciesView(request, id):
    try:
        existingPolicies = ExistingPolicies.objects.get(id=id)
    except ExistingPolicies.DoesNotExist:
        return Response(
            {"error": "ExistingPolicies details not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        serializer = ExistingPoliciesSerializer(existingPolicies)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = ExistingPoliciesSerializer(
            instance=existingPolicies, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def customUserDetail(request):
    if request.method == "GET":
        response = f"Hey {request.user}, you are seeing a GET response"
        return Response({"response": response}, status=status.HTTP_200_OK)
    elif request.method == "POST":
        text = request.POST.get("text")
        response = f"Hey {request.user} your text is {text}"
        return Response({"response": response}, status=status.HTTP_200_OK)
    return Response({}, status=status.HTTP_400_BAD_REQUEST)
