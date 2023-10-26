from django.db import models
from .country import Country



class College(models.Model):
    name = models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name