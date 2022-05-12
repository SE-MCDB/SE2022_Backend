from django.db import models


class Feedback(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    sex = models.IntegerField(blank=True, null=True)
    qtype = models.CharField(max_length=10)
    description = models.TextField()
    dataTime = models.DateTimeField(auto_now_add=True)