from django.db import models
from user_auth_app.models import UserProfile

class OrderCount(models.Model):
    order_count = models.IntegerField(default=0)

class RatingAndReview(models.Model):
    business_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    reviewer = models.IntegerField()
    rating = models.IntegerField(default=5)
    description = models.CharField(max_length=500, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

