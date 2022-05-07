from django.db import models

class Papers(models.Model):
    title = models.TextField()
    cites = models.IntegerField(default=0)
    pyear = models.IntegerField(blank=True, null=True)
    isEI = models.BooleanField(blank=True, null=True)
    isSCI = models.BooleanField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)