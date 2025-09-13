from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

# Create your views here.

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

@require_http_methods(["GET", "POST"])
@csrf_exempt
def user_list(request):
    """Handle user list operations"""
    if request.method == 'GET':
        # Sample user data
        users = [
            {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'},
            {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com'},
            {'id': 3, 'name': 'Bob Johnson', 'email': 'bob@example.com'}
        ]
        return JsonResponse({'users': users})
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            # In a real app, you would save to database here
            return JsonResponse({
                'message': 'User created successfully',
                'user': {
                    'id': 4,
                    'name': data.get('name', ''),
                    'email': data.get('email', '')
                }
            }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

@require_http_methods(["GET", "PUT", "DELETE"])
@csrf_exempt
def user_detail(request, user_id):
    """Handle individual user operations"""
    # Sample user data
    sample_user = {'id': user_id, 'name': f'User {user_id}', 'email': f'user{user_id}@example.com'}
    
    if request.method == 'GET':
        return JsonResponse({'user': sample_user})
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            # In a real app, you would update the database here
            updated_user = {
                'id': user_id,
                'name': data.get('name', sample_user['name']),
                'email': data.get('email', sample_user['email'])
            }
            return JsonResponse({
                'message': 'User updated successfully',
                'user': updated_user
            })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    elif request.method == 'DELETE':
        # In a real app, you would delete from database here
        return JsonResponse({
            'message': f'User {user_id} deleted successfully'
        })
