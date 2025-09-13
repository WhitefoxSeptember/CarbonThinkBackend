from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from datetime import datetime
from ..supabase_client import supabase_client

@require_http_methods(["GET", "POST"])
@csrf_exempt
def user_list(request):
    """Handle user list operations"""
    if request.method == 'GET':
        try:
            # Get all users from Supabase
            response = supabase_client.list_user_accounts()
            if response.data:
                return JsonResponse({'users': response.data})
            else:
                return JsonResponse({'users': []})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')
            
            # Validate required fields
            if not all([username, email, password]):
                return JsonResponse({
                    'error': 'Username, email, and password are required'
                }, status=400)
            
            # Check if user already exists by username
            existing_user = supabase_client.get_client().table('user_accounts').select('*').eq('username', username).execute()
            if existing_user.data:
                return JsonResponse({
                    'error': 'Username already exists'
                }, status=400)
            
            # Check if user already exists by email
            existing_email = supabase_client.get_client().table('user_accounts').select('*').eq('email', email).execute()
            if existing_email.data:
                return JsonResponse({
                    'error': 'Email already exists'
                }, status=400)
            
            # Create new user account in Supabase
            user_data = {
                'username': username,
                'email': email,
                'password_hash': password,  # In production, this should be hashed
                'first_name': first_name,
                'last_name': last_name,
                'date_joined': datetime.now().isoformat(),
                'is_active': True
            }
            
            response = supabase_client.create_user_account(user_data)
            
            if response.data:
                user = response.data[0]
                return JsonResponse({
                    'message': 'User created successfully',
                    'user': {
                        'id': user['id'],
                        'username': user['username'],
                        'email': user['email'],
                        'first_name': user['first_name'],
                        'last_name': user['last_name']
                    }
                }, status=201)
            else:
                return JsonResponse({'error': 'Failed to create user'}, status=500)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET", "PUT", "DELETE"])
@csrf_exempt
def user_detail(request, user_id):
    """Handle individual user operations"""
    try:
        # Get user from Supabase
        response = supabase_client.get_user_account(user_id)
        if not response.data:
            return JsonResponse({'error': 'User not found'}, status=404)
        user = response.data[0]
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    if request.method == 'GET':
        return JsonResponse({'user': user})
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            
            # Check if email is already taken by another user
            if 'email' in data:
                existing_email = supabase_client.get_client().table('user_accounts').select('*').eq('email', data['email']).neq('id', user_id).execute()
                if existing_email.data:
                    return JsonResponse({
                        'error': 'Email already exists'
                    }, status=400)
            
            # Update user in Supabase
            update_data = {}
            if 'email' in data:
                update_data['email'] = data['email']
            if 'first_name' in data:
                update_data['first_name'] = data['first_name']
            if 'last_name' in data:
                update_data['last_name'] = data['last_name']
            if 'is_active' in data:
                update_data['is_active'] = data['is_active']
            
            if update_data:
                response = supabase_client.update_user_account(user_id, update_data)
                if response.data:
                    updated_user = response.data[0]
                    return JsonResponse({
                        'message': 'User updated successfully',
                        'user': updated_user
                    })
                else:
                    return JsonResponse({'error': 'Failed to update user'}, status=500)
            else:
                return JsonResponse({'error': 'No valid fields to update'}, status=400)
                
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif request.method == 'DELETE':
        try:
            username = user.get('username', 'Unknown')
            response = supabase_client.delete_user_account(user_id)
            return JsonResponse({
                'message': f'User {username} (ID: {user_id}) deleted successfully'
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["POST"])
@csrf_exempt
def user_register(request):
    """Register a new user"""
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return JsonResponse({
                    'error': f'{field.capitalize()} is required'
                }, status=400)
        
        # Check if username already exists
        existing_username = supabase_client.get_client().table('user_accounts').select('*').eq('username', data['username']).execute()
        if existing_username.data:
            return JsonResponse({
                'error': 'Username already exists'
            }, status=400)
        
        # Check if email already exists
        existing_email = supabase_client.get_client().table('user_accounts').select('*').eq('email', data['email']).execute()
        if existing_email.data:
            return JsonResponse({
                'error': 'Email already exists'
            }, status=400)
        
        # Create new user in Supabase
        user_data = {
            'username': data['username'],
            'email': data['email'],
            'password_hash': data['password'],  # In production, hash this properly
            'first_name': data.get('first_name', ''),
            'last_name': data.get('last_name', ''),
            'is_active': True,
            'created_at': datetime.now().isoformat()
        }
        
        response = supabase_client.create_user_account(user_data)
        if response.data:
            user = response.data[0]
            return JsonResponse({
                'message': 'User registered successfully',
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'first_name': user['first_name'],
                    'last_name': user['last_name']
                }
            }, status=201)
        else:
            return JsonResponse({'error': 'Failed to create user'}, status=500)
        
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
        
        if not username or not password:
            return JsonResponse({
                'error': 'Username and password are required'
            }, status=400)
        
        # Find user by username
        user_response = supabase_client.get_client().table('user_accounts').select('*').eq('username', username).execute()
        
        if not user_response.data:
            return JsonResponse({
                'error': 'Invalid username or password'
            }, status=401)
        
        user = user_response.data[0]
        
        # In production, properly verify password hash
        if user['password_hash'] == password and user['is_active']:
            return JsonResponse({
                'message': 'Login successful',
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'first_name': user['first_name'],
                    'last_name': user['last_name']
                }
            })
        elif not user['is_active']:
            return JsonResponse({
                'error': 'Account is disabled'
            }, status=403)
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
        # With Supabase, logout is typically handled on the frontend
        # This endpoint can be used for any server-side cleanup if needed
        return JsonResponse({'message': 'Logout successful'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)