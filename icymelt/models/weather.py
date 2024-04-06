"""This module contains the model for weather conditions."""
from django.db import models


class WeatherCondition(models.Model):
    """A model to represent weather conditions."""
    weather = models.CharField(max_length=30)

    def __str__(self):
        return self.weather