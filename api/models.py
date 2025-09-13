from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    uid = models.CharField(max_length=100, blank=True, null=True)
    currentSources = models.ManyToManyField('CarbonSource', blank=True, related_name='user_profiles')

class CarbonSource(models.Model):
    name = models.CharField(max_length=100)
    uid = models.CharField(max_length=100,primary_key=True)
    description = models.CharField(max_length=100)
    sourceType = models.CharField(max_length=100)
    
class CarbonRecord(models.Model):
    uid = models.CharField(max_length=100,primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.ForeignKey(CarbonSource, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateField()
