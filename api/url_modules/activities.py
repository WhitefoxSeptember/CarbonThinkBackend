from django.urls import path
from ..views import activities

# User Activity URLs
# Handles user actions, tracking, logs, and activity history

app_name = 'activities'

urlpatterns = [
    # Activity tracking endpoints
    path('', activities.activity_list, name='activity_list'),
    path('<int:activity_id>/', activities.activity_detail, name='activity_detail'),
    path('stats/', activities.activity_stats, name='activity_stats'),
    # Future endpoints (to be implemented)
    # path('user/<int:user_id>/', views.user_activities, name='user_activities'),
    # path('log/', views.log_activity, name='log_activity'),
    # path('history/', views.activity_history, name='activity_history'),
]