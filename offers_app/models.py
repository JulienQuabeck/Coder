from django.db import models
from django.contrib.auth.models import User
from user_auth_app.models import UserProfile

class Feature(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.id, self.name

class OfferDetail(models.Model):

    types_title_Choices = [
        ('Basic Design', 'Basic Design'),
        ('Standard Design', 'Standard Design'),
        ('Premium Design', 'Premium Design'),
    ]

    types_Choices = [
        ('basic', 'basic'),
        ('standard', 'standard'),
        ('premium', 'premium'),
    ]

    title = models.CharField(max_length=255, default='Basic Design', choices=types_title_Choices)
    revisions = models.IntegerField(default=0) 
    delivery_time_in_days = models.IntegerField(default=0) 
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    features =  models.ManyToManyField(Feature, related_name="offers")
    offer_type = models.CharField(max_length=255, choices=types_Choices, default='basic')

class Offer(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to='offers/', null=True, blank=True)
    description = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    details = models.ManyToManyField(OfferDetail, related_name='offers')
    