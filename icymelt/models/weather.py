"""This module contains the model for weather conditions."""
from django.db import models


class WeatherCondition(models.Model):
    """A model to represent weather conditions."""
    code = models.IntegerField(null=True, unique=True)
    weather = models.CharField(max_length=100)

    def __str__(self):
        return self.weather
