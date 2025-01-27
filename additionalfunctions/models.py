from django.db import models

class OrderCount(models.Model):
    order_count = models.IntegerField(default=0)