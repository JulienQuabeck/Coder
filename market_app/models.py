# from django.db import models
# from django.contrib.auth.models import User

# class Offer(models.model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     image = ""
#     description = models.TextField(max_length=3000)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)
#     details = ""
#     min_price = models.DecimalField(max_digits=10, decimal_places=2)
#     min_delivery_time = models.IntegerField() 
#     user_details = ""