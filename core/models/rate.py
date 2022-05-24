from django.db import models
from .order import Order
from .user import User

class Rate(models.Model):
    rate_taste = models.IntegerField()
    rate_speed = models.IntegerField()
    rate_level = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    datetime = models.TextField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_rate")
    expert = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expert_rate")
    enterprise = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enterprise_rate")