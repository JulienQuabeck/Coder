from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    types_Choices = [
        ('business', 'Business'),
        ('customer', 'Customer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    location = models.CharField(max_length=255)
    tel = models.CharField(max_length=20) 
    description = models.TextField()
    working_hours = models.TextField()
    type = models.CharField(choices=types_Choices, default='customer', max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.type}"
    