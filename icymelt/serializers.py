from rest_framework import serializers
from .models import IceExp, Material, WeatherCondition


class IceExpSerializer(serializers.ModelSerializer):
    class Meta:
        model = IceExp
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class WeatherConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherCondition
        fields = '__all__'

