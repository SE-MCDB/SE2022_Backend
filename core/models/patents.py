from django.db import models


class Patents(models.Model):
    title = models.TextField()
    pyear = models.IntegerField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)