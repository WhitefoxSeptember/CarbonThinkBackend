from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CarbonFootprint(models.Model):
    """Model to track carbon footprint data"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carbon_footprints')
    activity_type = models.CharField(max_length=100, help_text="Type of activity (e.g., transportation, energy)")
    description = models.TextField(blank=True, help_text="Description of the activity")
    carbon_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Carbon footprint in kg CO2")
    date_recorded = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_recorded']
        verbose_name = 'Carbon Footprint'
        verbose_name_plural = 'Carbon Footprints'
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type}: {self.carbon_amount}kg CO2"

class Category(models.Model):
    """Model for categorizing carbon footprint activities"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    emission_factor = models.DecimalField(max_digits=8, decimal_places=4, help_text="Default emission factor for this category")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    """Extended user profile for carbon tracking"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    carbon_goal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Monthly carbon goal in kg CO2")
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def current_month_footprint(self):
        """Calculate current month's total carbon footprint"""
        from django.utils import timezone
        from datetime import datetime
        
        now = timezone.now()
        current_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        total = self.user.carbon_footprints.filter(
            date_recorded__gte=current_month
        ).aggregate(total=models.Sum('carbon_amount'))['total']
        
        return total or 0
