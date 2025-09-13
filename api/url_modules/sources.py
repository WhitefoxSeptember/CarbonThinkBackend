from django.urls import path
from ..views import sources

# Carbon Footprint Source Management URLs
# Handles carbon sources, calculations, and footprint data

app_name = 'sources'

urlpatterns = [
    # Carbon footprint source endpoints
    path('', sources.source_list, name='source_list'),
    path('<int:source_id>/', sources.source_detail, name='source_detail'),
    path('categories/', sources.source_categories, name='source_categories'),
    path('calculate/', sources.calculate_footprint, name='calculate_footprint'),
    
    # User source management endpoints
    path('user/add/', sources.add_source_to_user, name='add_source_to_user'),
    path('user/records/', sources.get_user_records_by_timeframe, name='get_user_records_by_timeframe'),
    path('user/remove/', sources.remove_source_from_user, name='remove_source_from_user'),
    path('user/sources/', sources.get_user_sources, name='get_user_sources'),
    
    # Future endpoints (to be implemented)
    # path('user/<int:user_id>/footprint/', views.user_footprint, name='user_footprint'),
    # path('reports/', views.footprint_reports, name='footprint_reports'),
    # path('emissions/', views.emission_factors, name='emission_factors'),
]