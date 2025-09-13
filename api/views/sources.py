from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from ..supabase_client import supabase_client

@require_http_methods(["GET", "POST"])
@csrf_exempt
def source_list(request):
    """Handle carbon source list operations"""
    if request.method == 'GET':
        try:
            # Get carbon sources from Supabase
            response = supabase_client.get_client().table('carbon_sources').select('*').execute()
            sources = response.data or []
            return JsonResponse({'sources': sources})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['name', 'category', 'emission_factor']
            for field in required_fields:
                if field not in data or data[field] is None:
                    return JsonResponse({
                        'error': f'{field.capitalize()} is required'
                    }, status=400)
            
            # Create carbon source in Supabase
            source_data = {
                'name': data['name'],
                'category': data['category'],
                'emission_factor': float(data['emission_factor']),
                'description': data.get('description', ''),
                'unit': data.get('unit', 'kg CO2')
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
        except ValueError:
            return JsonResponse({'error': 'Invalid emission factor value'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET", "PUT", "DELETE"])
@csrf_exempt
def source_detail(request, source_id):
    """Handle individual carbon source operations"""
    try:
        # Get carbon source from Supabase
        response = supabase_client.get_client().table('carbon_sources').select('*').eq('id', source_id).execute()
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
            if 'category' in data:
                update_data['category'] = data['category']
            if 'emission_factor' in data:
                update_data['emission_factor'] = float(data['emission_factor'])
            if 'description' in data:
                update_data['description'] = data['description']
            if 'unit' in data:
                update_data['unit'] = data['unit']
            
            if update_data:
                # Update carbon source in Supabase
                response = supabase_client.get_client().table('carbon_sources').update(update_data).eq('id', source_id).execute()
                
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
        except ValueError:
            return JsonResponse({'error': 'Invalid emission factor value'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif request.method == 'DELETE':
        try:
            # Delete carbon source from Supabase
            response = supabase_client.get_client().table('carbon_sources').delete().eq('id', source_id).execute()
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
        
        # Get carbon source from Supabase to fetch emission factor
        source_response = supabase_client.get_client().table('carbon_sources').select('*').eq('id', source_id).execute()
        
        if not source_response.data:
            return JsonResponse({'error': 'Carbon source not found'}, status=404)
        
        source = source_response.data[0]
        emission_factor = float(source['emission_factor'])
        
        # Calculate carbon footprint
        carbon_footprint = float(activity_amount) * emission_factor
        
        return JsonResponse({
            'carbon_footprint': carbon_footprint,
            'unit': source.get('unit', 'kg CO2'),
            'calculation': {
                'amount': activity_amount,
                'emission_factor': emission_factor,
                'source_id': source_id,
                'source_name': source['name']
            }
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except ValueError:
        return JsonResponse({'error': 'Invalid numeric values'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)