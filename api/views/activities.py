from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import datetime
import json
from ..models import CarbonRecord

@require_http_methods(["POST"])
@csrf_exempt
def carbon_consumption(request):
    """Get total carbon consumption for a user within a timeframe"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        # Validate required fields
        if not username:
            return JsonResponse({'error': 'Username is required'}, status=400)
        if not start_date or not end_date:
            return JsonResponse({'error': 'Both start_date and end_date are required'}, status=400)
        
        # Validate user exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        # Parse dates
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
        
        # Validate date range
        if start_date_obj > end_date_obj:
            return JsonResponse({'error': 'Start date cannot be after end date'}, status=400)
        
        # Query carbon records for the user within the timeframe
        records = CarbonRecord.objects.filter(
            user=user,
            date__gte=start_date_obj,
            date__lte=end_date_obj
        )
        
        # Calculate total carbon consumption
        total_consumption = records.aggregate(total=Sum('amount'))['total'] or 0
        record_count = records.count()
        
        return JsonResponse({
            'username': username,
            'timeframe': {
                'start_date': start_date,
                'end_date': end_date
            },
            'total_carbon_consumption': float(total_consumption),
            'record_count': record_count,
            'message': f'Found {record_count} records with total consumption of {total_consumption} units'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Internal server error: {str(e)}'}, status=500)