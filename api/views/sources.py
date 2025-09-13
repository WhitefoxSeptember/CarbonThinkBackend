from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import uuid
from ..supabase_client import supabase_client

@require_http_methods(["GET", "POST"])
@csrf_exempt
def source_list(request):
    """Handle carbon source list operations"""
    if request.method == 'GET':
        try:
            # Get carbon sources from Supabase (excluding emission_factor and unit)
            response = supabase_client.get_client().table('carbon_sources').select('uid, name, description, source_type, created_at, updated_at').execute()
            sources = response.data or []
            return JsonResponse({'sources': sources})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['name', 'source_type']
            for field in required_fields:
                if field not in data or data[field] is None:
                    return JsonResponse({
                        'error': f'{field.replace("_", " ").capitalize()} is required'
                    }, status=400)
            
            # Create carbon source in Supabase
            source_data = {
                'uid': str(uuid.uuid4()),
                'name': data['name'],
                'source_type': data['source_type'],
                'description': data.get('description', '')
            }
            
            response = supabase_client.get_client().table('carbon_sources').insert(source_data).execute()
            
            if response.data:
                return JsonResponse({
                    'message': 'Carbon source created successfully',
                    'source': response.data[0]
                }, status=201)
            else:
                return JsonResponse({'error': 'Failed to create carbon source'}, status=500)
                
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET", "PUT", "DELETE"])
@csrf_exempt
def source_detail(request, source_id):
    """Handle individual carbon source operations"""
    try:
        # Get carbon source from Supabase (excluding emission_factor and unit)
        response = supabase_client.get_client().table('carbon_sources').select('uid, name, description, source_type, created_at, updated_at').eq('uid', source_id).execute()
        if not response.data:
            return JsonResponse({'error': 'Carbon source not found'}, status=404)
        
        source = response.data[0]
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    if request.method == 'GET':
        return JsonResponse({'source': source})
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            
            # Prepare update data
            update_data = {}
            if 'name' in data:
                update_data['name'] = data['name']
            if 'source_type' in data:
                update_data['source_type'] = data['source_type']
            if 'description' in data:
                update_data['description'] = data['description']
            
            if update_data:
                # Update carbon source in Supabase
                response = supabase_client.get_client().table('carbon_sources').update(update_data).eq('uid', source_id).execute()
                
                if response.data:
                    return JsonResponse({
                        'message': 'Carbon source updated successfully',
                        'source': response.data[0]
                    })
                else:
                    return JsonResponse({'error': 'Failed to update carbon source'}, status=500)
            else:
                return JsonResponse({'error': 'No valid fields to update'}, status=400)
                
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif request.method == 'DELETE':
        try:
            # Delete carbon source from Supabase
            response = supabase_client.get_client().table('carbon_sources').delete().eq('uid', source_id).execute()
            return JsonResponse({
                'message': f'Carbon source {source_id} deleted successfully'
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
@csrf_exempt
def source_categories(request):
    """Get carbon source categories"""
    # Placeholder for source categories
    categories = [
        {'name': 'transportation', 'description': 'Vehicle and travel emissions'},
        {'name': 'energy', 'description': 'Electricity and heating emissions'},
        {'name': 'food', 'description': 'Food production and consumption emissions'},
        {'name': 'waste', 'description': 'Waste disposal and recycling emissions'}
    ]
    return JsonResponse({'categories': categories})

@require_http_methods(["POST"])
@csrf_exempt
def calculate_footprint(request):
    """Calculate carbon footprint based on activity and source"""
    try:
        data = json.loads(request.body)
        activity_amount = data.get('amount', 0)
        source_id = data.get('source_id')
        
        # Validate required fields
        if not source_id:
            return JsonResponse({'error': 'Source ID is required'}, status=400)
        
        if not activity_amount or activity_amount <= 0:
            return JsonResponse({'error': 'Valid activity amount is required'}, status=400)
        
        # Get carbon source from Supabase to verify it exists
        source_response = supabase_client.get_client().table('carbon_sources').select('*').eq('uid', source_id).execute()
        
        if not source_response.data:
            return JsonResponse({'error': 'Carbon source not found'}, status=404)
        
        source = source_response.data[0]
        
        # Simple calculation using a default emission factor based on category
        category_factors = {
            'transportation': 0.21,  # kg CO2 per km
            'energy': 0.45,         # kg CO2 per kWh
            'food': 2.5,            # kg CO2 per kg
            'waste': 0.5            # kg CO2 per kg
        }
        
        default_factor = category_factors.get(source['source_type'].lower(), 1.0)
        carbon_footprint = float(activity_amount) * default_factor
        
        return JsonResponse({
            'carbon_footprint': carbon_footprint,
            'unit': 'kg CO2',
            'calculation': {
                'amount': activity_amount,
                'default_factor': default_factor,
                'source_id': source_id,
                'source_name': source['name'],
                'source_type': source['source_type']
            }
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except ValueError:
        return JsonResponse({'error': 'Invalid numeric values'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["POST"])
@csrf_exempt
def add_source_to_user(request):
    """Add a source to user profile"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        source_uid = data.get('source_uid')
        
        # Validate required fields
        if not username:
            return JsonResponse({'error': 'Username is required'}, status=400)
        if not source_uid:
            return JsonResponse({'error': 'Source UID is required'}, status=400)
        
        # Get user account
        user_response = supabase_client.get_client().table('user_accounts').select('*').eq('username', username).execute()
        if not user_response.data:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        user_id = user_response.data[0]['id']
        
        # Check if source exists
        source_response = supabase_client.get_client().table('carbon_sources').select('*').eq('uid', source_uid).execute()
        if not source_response.data:
            return JsonResponse({'error': 'Source not found'}, status=404)
        
        # Get or create user profile
        profile_response = supabase_client.get_client().table('user_profiles').select('*').eq('user_id', user_id).execute()
        if not profile_response.data:
            # Create user profile
            profile_data = {'user_id': user_id}
            profile_response = supabase_client.get_client().table('user_profiles').insert(profile_data).execute()
            if not profile_response.data:
                return JsonResponse({'error': 'Failed to create user profile'}, status=500)
            profile_id = profile_response.data[0]['id']
        else:
            profile_id = profile_response.data[0]['id']
        
        # Check if source is already added to user profile
        existing_response = supabase_client.get_client().table('user_profile_sources').select('*').eq('user_profile_id', profile_id).eq('carbon_source_uid', source_uid).execute()
        if existing_response.data:
            return JsonResponse({'error': 'Source already added to user profile'}, status=400)
        
        # Add source to user profile
        profile_source_data = {
            'user_profile_id': profile_id,
            'carbon_source_uid': source_uid
        }
        result = supabase_client.get_client().table('user_profile_sources').insert(profile_source_data).execute()
        
        if result.data:
            return JsonResponse({
                'message': 'Source added to user profile successfully',
                'data': result.data[0]
            }, status=201)
        else:
            return JsonResponse({'error': 'Failed to add source to user profile'}, status=500)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
@csrf_exempt
def get_user_records_by_timeframe(request):
    """Get user records by timeframe and source"""
    try:
        username = request.GET.get('username')
        source_uid = request.GET.get('source_uid')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        # Validate required fields
        if not username:
            return JsonResponse({'error': 'Username is required'}, status=400)
        if not source_uid:
            return JsonResponse({'error': 'Source UID is required'}, status=400)
        if not start_date or not end_date:
            return JsonResponse({'error': 'Start date and end date are required'}, status=400)
        
        # Get user account
        user_response = supabase_client.get_client().table('user_accounts').select('*').eq('username', username).execute()
        if not user_response.data:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        user_id = user_response.data[0]['id']
        
        # Get user profile
        profile_response = supabase_client.get_client().table('user_profiles').select('*').eq('user_id', user_id).execute()
        if not profile_response.data:
            return JsonResponse({'error': 'User profile not found'}, status=404)
        
        profile_id = profile_response.data[0]['id']
        
        # Get carbon records for the user, source, and timeframe
        records_response = supabase_client.get_client().table('carbon_records').select('*').eq('user_profile_id', profile_id).eq('carbon_source_uid', source_uid).gte('date', start_date).lte('date', end_date).execute()
        
        records = records_response.data or []
        
        return JsonResponse({
            'records': records,
            'count': len(records),
            'timeframe': {
                'start_date': start_date,
                'end_date': end_date
            }
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["DELETE"])
@csrf_exempt
def remove_source_from_user(request):
    """Remove a source from user profile"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        source_uid = data.get('source_uid')
        
        # Validate required fields
        if not username:
            return JsonResponse({'error': 'Username is required'}, status=400)
        if not source_uid:
            return JsonResponse({'error': 'Source UID is required'}, status=400)
        
        # Get user account
        user_response = supabase_client.get_client().table('user_accounts').select('*').eq('username', username).execute()
        if not user_response.data:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        user_id = user_response.data[0]['id']
        
        # Get user profile
        profile_response = supabase_client.get_client().table('user_profiles').select('*').eq('user_id', user_id).execute()
        if not profile_response.data:
            return JsonResponse({'error': 'User profile not found'}, status=404)
        
        profile_id = profile_response.data[0]['id']
        
        # Check if source exists in user profile
        existing_response = supabase_client.get_client().table('user_profile_sources').select('*').eq('user_profile_id', profile_id).eq('carbon_source_uid', source_uid).execute()
        if not existing_response.data:
            return JsonResponse({'error': 'Source not found in user profile'}, status=404)
        
        # Remove source from user profile
        result = supabase_client.get_client().table('user_profile_sources').delete().eq('user_profile_id', profile_id).eq('carbon_source_uid', source_uid).execute()
        
        return JsonResponse({
            'message': 'Source removed from user profile successfully'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
@csrf_exempt
def get_user_sources(request):
    """Get all sources in user's profile"""
    try:
        username = request.GET.get('username')
        
        # Validate required fields
        if not username:
            return JsonResponse({'error': 'Username is required'}, status=400)
        
        # Get user account
        user_response = supabase_client.get_client().table('user_accounts').select('*').eq('username', username).execute()
        if not user_response.data:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        user_id = user_response.data[0]['id']
        
        # Get user profile
        profile_response = supabase_client.get_client().table('user_profiles').select('*').eq('user_id', user_id).execute()
        if not profile_response.data:
            return JsonResponse({'error': 'User profile not found'}, status=404)
        
        profile_id = profile_response.data[0]['id']
        
        # Get user's sources via join
        sources_response = supabase_client.get_client().table('user_profile_sources').select('carbon_source_uid, carbon_sources(*)').eq('user_profile_id', profile_id).execute()
        
        sources = []
        if sources_response.data:
            for item in sources_response.data:
                if item.get('carbon_sources'):
                    sources.append(item['carbon_sources'])
        
        return JsonResponse({
            'sources': sources,
            'count': len(sources)
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)