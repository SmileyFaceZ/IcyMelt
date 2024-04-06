"""Import admin class from django"""
from django.contrib import admin
from icymelt.models import Material, WeatherCondition, IceExp


# Register your models here.

admin.site.register(Material)
admin.site.register(WeatherCondition)
admin.site.register(IceExp)
