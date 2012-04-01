from django.db import models

class Problem(models.Model):

    slug = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=32)
    number_in_problem = models.IntegerField()

    def __str__(self):
        return self.name
