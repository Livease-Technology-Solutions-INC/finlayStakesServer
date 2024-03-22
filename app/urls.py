from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenRefreshView
from app import views

urlpatterns = [
    path("users/", CustomUserView.as_view(), name="custom_user_list"),
    path("user/", views.customUserDetail, name="custom-user-detail"),
    path("token/", MyTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("register/", CustomUserRegistrationView.as_view(), name="register"),
    path("verify-email/<str:email>/", VerifyEmailView.as_view(), name="verify-email"),
    path("resend_otp/<str:email>/", ResendOTPView.as_view(), name="resend_otp"),
    path(
        "request-password-reset/",
        views.request_password_reset,
        name="request_password_reset",
    ),
    path("reset-password/<str:uidb64>/<str:token>/", views.reset_password, name="reset_password"),
    path(
        "personal_details/<int:id>/",
        views.PersonalDetailsView,
        name="personal_details_list",
    ),
    path(
        "income_details/<int:id>/",
        views.IncomeDetailsView,
        name="income_details_list",
    ),
    path(
        "expense_details/<int:id>/",
        views.ExpenseDetailsView,
        name="expense_details_list",
    ),
    path("asset_details/<int:id>/", views.AssetDetailsView, name="asset_details_list"),
    path(
        "liability_details/<int:id>/",
        views.LiabilityDetailsView,
        name="liability_details_list",
    ),
    path("goals/<int:id>/", views.GoalsView, name="goals_list"),
    path(
        "existing_provisions_details/<int:id>/",
        views.ExistingProvisionsDetailsView,
        name="existing_provision_detail_list",
    ),
    path(
        "financial_planning_shortfall/<int:id>/",
        views.FinancialPlanningShortfallView,
        name="financial_planning_shortfall",
    ),
    path(
        "existing_policies/<int:id>/",
        views.ExistingPoliciesView,
        name="existing_policies",
    ),
]
