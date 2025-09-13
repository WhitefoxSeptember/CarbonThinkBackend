from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from datetime import datetime
import json
from ..supabase_client import supabase_client

@require_http_methods(["POST"])
@csrf_exempt
def carbon_consumption(request):
    """Get total carbon consumption for a user within a timeframe"""
    try:
        data = json.loads(request.body)
        email = data.get('email')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        # Validate required fields
        if not email:
            return JsonResponse({'error': 'Email is required'}, status=400)
        if not start_date or not end_date:
            return JsonResponse({'error': 'Both start_date and end_date are required'}, status=400)
        
        # Validate user exists in Supabase by email
        user_response = supabase_client.get_client().table('user_accounts').select('*').eq('email', email).execute()
        if not user_response.data:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        user = user_response.data[0]
        user_id = user['id']
        
        # Parse dates
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
        
        # Validate date range
        if start_date_obj > end_date_obj:
            return JsonResponse({'error': 'Start date cannot be after end date'}, status=400)
        
        # Query carbon records from Supabase for the user within the timeframe
        records_response = supabase_client.get_client().table('carbon_records').select('*').eq('user_id', user_id).gte('date', start_date).lte('date', end_date).execute()
        
        records = records_response.data or []
        
        # Calculate total carbon consumption
        total_consumption = sum(float(record.get('amount', 0)) for record in records)
        record_count = len(records)
        
        return JsonResponse({
            'email': email,
            'timeframe': {
                'start_date': start_date,
                'end_date': end_date
            },
            'total_carbon_consumption': total_consumption,
            'record_count': record_count,
            'message': f'Found {record_count} records with total consumption of {total_consumption} units'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Internal server error: {str(e)}'}, status=500)