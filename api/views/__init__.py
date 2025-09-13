# Import all views for backward compatibility
from .accounts import (
    user_list,
    user_detail,
    user_register,
    user_login,
    user_logout
)
from .activities import *
from .sources import *

# Keep the original views for backward compatibility
from django.http import JsonResponse

def index(request):
    """API root endpoint"""
    return JsonResponse({
        'message': 'Welcome to CarbonThink API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health/',
            'users': '/api/users/',
            'user_detail': '/api/users/<id>/'
        }
    })

def health_check(request):
    """Health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'API is running successfully'
    })