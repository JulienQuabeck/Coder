from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):

    types_Choices = [
        ('business', 'Business'),
        ('customer', 'Customer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    username = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    repeated_password = models.CharField(max_length=255)
    type = models.CharField(choices=types_Choices, default='customer', max_length=8)

    def __str__(self):
        return f"{self.user.username} - {self.type}"