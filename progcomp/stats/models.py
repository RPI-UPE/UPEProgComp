from django.db import models

class Report(models.Model):
    view = models.CharField(max_length=50)
    method = models.CharField(max_length=10)
    calls = models.IntegerField()
    time = models.FloatField()
