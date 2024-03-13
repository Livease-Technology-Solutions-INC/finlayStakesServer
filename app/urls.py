from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenRefreshView
from app import views

urlpatterns = [
    path('users/', CustomUserView.as_view(), name='custom_user_list'),
    path('user/', views.customUserDetail, name='custom-user-detail'),
    path('personal_details/', PersonalDetailsView.as_view(), name='personal_details_list'),
    path('token/', MyTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('register/', CustomUserRegistrationView.as_view(), name='register'),
    path('test/', views.testEndPoint, name='test'),    
]