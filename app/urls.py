from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('users/', CustomUserView.as_view(), name='custom_user_list'),
    path('user/', CustomUserDetailView.as_view(), name='custom-user-detail'),
    path('personal_details/', PersonalDetailsView.as_view(), name='personal_details_list'),
    path('login/', CustomUserLoginView.as_view(), name='login'),
    path('register/', CustomUserRegistrationView.as_view(), name='register'),
    path('logout/', CustomUserLogoutView.as_view(), name='logout'),
    
]