"""This module contains the ice experiment model."""
from django.db import models
from icymelt.models.weather import WeatherCondition
import datetime
import requests


def get_current_weather():
    url = 'https://api.weatherapi.com/v1/current.json'
    params = {
        'key': config('API_KEY'),
        'q': 'Bangkok'
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data


weather_api_data = get_current_weather()


class IceExp(models.Model):
    """A model to represent ice experiment data."""
    date = models.DateTimeField(default=datetime.datetime.now())
    temp = models.DecimalField(default=weather_api_data['current']['temp_c'], max_digits=5, decimal_places=2)
    humidity = models.DecimalField(default=weather_api_data['current']['humidity'], max_digits=5, decimal_places=2)
    weather_cond = models.ForeignKey('WeatherCondition', on_delete=models.CASCADE)
    thickness = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    material = models.ForeignKey('Material', on_delete=models.CASCADE)
    duration = models.DecimalField(max_digits=5, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.weather_cond_id:
            default_weather_condition_code = weather_api_data['current']['condition']['code']
            try:
                default_weather_condition = WeatherCondition.objects.get(
                    code=default_weather_condition_code)
                self.weather_cond = default_weather_condition
            except WeatherCondition.DoesNotExist:
                print(f"Error: Weather condition with code {default_weather_condition_code} does not exist.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} - {self.temp} - {self.humidity} - {self.material} - {self.duration}"