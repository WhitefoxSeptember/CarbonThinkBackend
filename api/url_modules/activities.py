from django.urls import path
from ..views import activities

# User Activity URLs
# Single endpoint for carbon consumption tracking

app_name = 'activities'

urlpatterns = [
    # Carbon consumption endpoint
    path('carbon-consumption/', activities.carbon_consumption, name='carbon_consumption'),
]