from rest_framework import serializers
from .models import IceExp, Material, WeatherCondition


class IceExpSerializer(serializers.ModelSerializer):
    class Meta:
        model = IceExp
        fields = ['id', 'temp', 'humidity']