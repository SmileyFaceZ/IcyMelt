"""This module contains the ice experiment model."""
from django.db import models
import datetime


class IceExp(models.Model):
    """A model to represent ice experiment data."""
    date = models.DateField(auto_now_add=datetime.date.today())
    temp = models.DecimalField(max_digits=5, decimal_places=2)
    humidity = models.DecimalField(max_digits=5, decimal_places=2)
    windspeed = models.DecimalField(max_digits=5, decimal_places=2)
    weather_cond = models.ForeignKey('WeatherCondition', on_delete=models.CASCADE)
    thickness = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    material = models.ForeignKey('Material', on_delete=models.CASCADE)
    duration = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.date} - {self.temp} - {self.weight} - {self.material} - {self.duration}"