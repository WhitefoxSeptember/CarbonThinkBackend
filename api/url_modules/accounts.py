from django.urls import path
from ..views import accounts

# User Account Management URLs
# Handles user registration, login, profile management, authentication

app_name = 'accounts'

urlpatterns = [
    # User management endpoints
    path('users/', accounts.user_list, name='user_list'),
    path('users/<int:user_id>/', accounts.user_detail, name='user_detail'),
    
    # Authentication endpoints
    path('register/', accounts.user_register, name='user_register'),
    path('login/', accounts.user_login, name='user_login'),
    path('logout/', accounts.user_logout, name='user_logout'),
    # path('profile/', views.user_profile, name='user_profile'),
    # path('change-password/', views.change_password, name='change_password'),
]