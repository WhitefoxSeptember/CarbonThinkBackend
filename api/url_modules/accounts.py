from django.urls import path
from .. import views

# User Account Management URLs
# Handles user registration, login, profile management, authentication

app_name = 'accounts'

urlpatterns = [
    # User management endpoints
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    
    # Authentication endpoints (to be implemented)
    # path('register/', views.user_register, name='user_register'),
    # path('login/', views.user_login, name='user_login'),
    # path('logout/', views.user_logout, name='user_logout'),
    # path('profile/', views.user_profile, name='user_profile'),
    # path('change-password/', views.change_password, name='change_password'),
]