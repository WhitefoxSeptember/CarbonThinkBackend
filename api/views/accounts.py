from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json

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

@require_http_methods(["POST"])
@csrf_exempt
def user_register(request):
    """Handle user registration"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        # Validate required fields
        if not all([username, email, password]):
            return JsonResponse({
                'error': 'Username, email, and password are required'
            }, status=400)
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'error': 'Username already exists'
            }, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'error': 'Email already exists'
            }, status=400)
        
        # Create new user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        return JsonResponse({
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["POST"])
@csrf_exempt
def user_login(request):
    """Handle user login"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        # Validate required fields
        if not all([username, password]):
            return JsonResponse({
                'error': 'Username and password are required'
            }, status=400)
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            })
        else:
            return JsonResponse({
                'error': 'Invalid username or password'
            }, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["POST"])
@csrf_exempt
def user_logout(request):
    """Handle user logout"""
    try:
        logout(request)
        return JsonResponse({
            'message': 'Logout successful'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)