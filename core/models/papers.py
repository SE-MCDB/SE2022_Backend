from django.db import models

class Papers(models.Model):
    title = models.TextField()
    cites = models.IntegerField(default=0)
    pyear = models.IntegerField()
    isEI = models.BooleanField()
    isSCI = models.BooleanField()