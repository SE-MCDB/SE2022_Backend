from django.db import models

class Patents:
    title = models.TextField()
    pyear = models.IntegerField()