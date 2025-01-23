from django.db import models
from user_auth_app.models import UserProfile

class Orders(models.Model):

    types_Choices = [
        ('basic', 'basic'),
        ('standard', 'standard'),
        ('premium', 'premium'),
    ]

    status_Choices = [
        ('in_progres', 'in_progress'),
        ('completed', 'completed')
    ]

    customer_user = models.IntegerField(default=0) # evtl. ändern
    business_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    revisions = models.IntegerField(default=0) 
    delivery_time_in_days = models.IntegerField(default=0) 
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    features = models.JSONField(default=dict, blank=True)
    offer_type = models.CharField(max_length=255, choices=types_Choices, default='basic')
    status = models.CharField(max_length=255, choices=status_Choices, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)