from django.db import models
from user_auth_app.models import UserProfile
from offers_app.models import OfferDetail

class Orders(models.Model):

    status_Choices = [
        ('in_progress', 'in_progress'),
        ('completed', 'completed')
    ]

    customer_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    business_user = models.IntegerField(default=0)
    offer_detail_id = models.ForeignKey(OfferDetail, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=status_Choices, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderDetail(models.Model):
        
    status_Choices = [
        ('in_progress', 'in_progress'),
        ('completed', 'completed'),
        ('cancelled', 'cancelled')
    ]

    customer_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    business_user = models.IntegerField()
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField()
    offer_type = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=status_Choices, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)