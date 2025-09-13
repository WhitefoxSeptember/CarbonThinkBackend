from django.urls import path, include
from . import views

urlpatterns = [
    # API root and health check
    path('', views.index, name='api_root'),
    path('health/', views.health_check, name='health_check'),
    
    # Include category-specific URL modules
    path('accounts/', include('api.url_modules.accounts')),
    path('activities/', include('api.url_modules.activities')),
    path('sources/', include('api.url_modules.sources')),
]