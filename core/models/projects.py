from django.db import models

class Projects:
    title = models.TextField()
    startYear = models.IntegerField()
    endYear = models.IntegerField(blank=True, null=True)
    typeFirst = models.TextField(blank=True, null=True)
    typeSecond = models.TextField(blank=True, null=True)
    typeThird = models.TextField(blank=True, null=True)