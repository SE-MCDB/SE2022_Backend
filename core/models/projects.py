from django.db import models


class Projects(models.Model):
    title = models.TextField()
    startYear = models.IntegerField(blank=True, null=True)
    endYear = models.IntegerField(blank=True, null=True)
    typeFirst = models.TextField(blank=True, null=True)
    typeSecond = models.TextField(blank=True, null=True)
    typeThird = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)