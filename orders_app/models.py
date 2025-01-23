from django.db import models
from user_auth_app.models import UserProfile

class Orders(models.Model):

    status_Choices = [
        ('in_progres', 'in_progress'),
        ('completed', 'completed')
    ]

    customer_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    business_user = models.IntegerField(default=0)
    offer_detail_id = models.IntegerField(default=0)
    status = models.CharField(max_length=255, choices=status_Choices, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)