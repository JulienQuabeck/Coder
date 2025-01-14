from django.db import models
from django.contrib.auth.models import User
from user_auth_app.models import UserProfile

class OfferDetail(models.Model):
    url = models.URLField()
    
    def __str__(self):
        return f"Detail URL: {self.url}"

class Offer(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to='offers/', null=True, blank=True)
    description = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    details = models.ManyToManyField(OfferDetail, related_name='offers')
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    min_delivery_time = models.IntegerField() 
    user_details = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_offers')