from django.db import models
# from django.contrib.auth.models import User

class BaseInfo(models.Model):
    review_count = models.IntegerField() 
    average_rating = models.DecimalField(max_digits=2, decimal_places=1)
    businiess_profile_count = models.IntegerField() 
    offer_count = models.IntegerField() 