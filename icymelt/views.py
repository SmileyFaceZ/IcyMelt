from django.views.generic import TemplateView
from django.db.models import Avg, Sum, Min, Max, Count
from django.contrib.postgres.aggregates import ArrayAgg
from decouple import config
from decimal import Decimal
from icymelt.serializers import IceExpSerializer, MaterialSerializer, WeatherConditionSerializer
from icymelt.models import IceExp, Material, WeatherCondition
from rest_framework import generics
from collections import defaultdict, OrderedDict
from rest_framework.response import Response
from rest_framework.views import APIView
<<<<<<< HEAD
from django.db.models import Avg, Sum, Min, Max, Count
from django.urls import get_resolver, get_mod_func
from django.shortcuts import render
from . import urls
=======
import requests
>>>>>>> 9d1260efd4547f3c94d26f726cb6798ed6938c83


def get_current_weather():
    url = 'https://api.weatherapi.com/v1/current.json'
    params = {
        'key': config('API_KEY'),
        'q': 'Bangkok'
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data


class HomeView(TemplateView):
    template_name = "icymelt/home.html"
    data = get_current_weather()

    @staticmethod
    def get_cur_temp():
        return HomeView.data['current']['temp_c']

    @staticmethod
    def get_cur_rh():
        return HomeView.data['current']['humidity']

    @staticmethod
    def get_cur_condition():
        return HomeView.data['current']['condition']['text']

    @staticmethod
    def get_cur_wind():
        return HomeView.data['current']['wind_kph']

    @staticmethod
    def get_pie_chart_data():
        material_counts = IceExp.objects.values('material').annotate(
            count=Count('id'))
        material_count_dict = {
            str(Material.objects.get(id=material['material'])): material[
                'count']
            for material in material_counts}

        labels = list(material_count_dict.keys())
        data = list(material_count_dict.values())

        return labels, data

    def group_ice_object(self, date_list):
        ice_exp_by_date = defaultdict(list)
        for ice_exp in IceExp.objects.filter(date__date__in=date_list):
            ice_exp_by_date[ice_exp.date.date()].append(ice_exp)
        return ice_exp_by_date

    def get_series(self, materials, sorted_average_durations):
        series = []
        for material in materials:
            data = []
            for date, durations in sorted_average_durations.items():
                duration = durations[material]
                if duration is None:
                    duration = Decimal('0')
                data.append(str(round(duration, 2)))

            series.append({'name': material.type, 'data': data})
        return series

    def get_average_duration_by_date(self, date_list, materials):
        average_durations_by_date = defaultdict(dict)
        ice_exp_by_date = self.group_ice_object(date_list)
        for date, ice_exp_objects in ice_exp_by_date.items():
            average_durations_for_date = {}

            for material in materials:
                ice_exp_objects_for_material = [exp for exp in ice_exp_objects
                                                if exp.material == material]

                average_duration = None
                if ice_exp_objects_for_material:
                    average_duration = sum(exp.duration for exp in
                                           ice_exp_objects_for_material) / len(
                        ice_exp_objects_for_material)

                average_durations_for_date[material] = average_duration

            average_durations_by_date[date] = average_durations_for_date
        return average_durations_by_date

    def get_line_plot_data(self):
        date_list = list(
            IceExp.objects.order_by('date').values_list('date',
                                                        flat=True).distinct())

        materials = Material.objects.all()
        average_durations_by_date = self.get_average_duration_by_date(date_list, materials)

        sorted_average_durations = OrderedDict(
            sorted(average_durations_by_date.items()))

        materials = set(
            material for durations in sorted_average_durations.values() for material
            in durations.keys())

        series = self.get_series(materials, sorted_average_durations)

        categories = [date.strftime('%Y-%m-%d') for date in sorted_average_durations.keys()]
        return series, categories

    def get_average_data(self, feature):
        data = IceExp.objects.all().aggregate(avg=Avg(feature))['avg']
        data = round(data, 2)
        return data

    def get_min_data(self, feature):
        data = IceExp.objects.all().aggregate(min=Min(feature))['min']
        data = round(data, 2)
        return data

    def get_max_data(self, feature):
        data = IceExp.objects.all().aggregate(max=Max(feature))['max']
        data = round(data, 2)
        return data

    def get_scatter_plot_data(self, field_name):
        data = []
        for material in Material.objects.all():
            mat = {
                'name': material.type,
                'data': []
            }
            for ice_exp in IceExp.objects.filter(material=material):
                mat['data'].append([float(getattr(ice_exp, field_name)),
                                    int(ice_exp.duration),
                                    float(ice_exp.weight)])
            data.append(mat)

        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['avg_temp'] = self.get_average_data('temp')
        context['min_temp'] = self.get_min_data('temp')
        context['max_temp'] = self.get_max_data('temp')

        context['avg_rh'] = self.get_average_data('humidity')
        context['min_rh'] = self.get_min_data('humidity')
        context['max_rh'] = self.get_max_data('humidity')

        context['avg_thickness'] = self.get_average_data('thickness')
        context['min_thickness'] = self.get_min_data('thickness')
        context['max_thickness'] = self.get_max_data('thickness')

        context['avg_weight'] = self.get_average_data('weight')
        context['min_weight'] = self.get_min_data('weight')
        context['max_weight'] = self.get_max_data('weight')

        context['avg_duration'] = self.get_average_data('duration')
        context['min_duration'] = self.get_min_data('duration')
        context['max_duration'] = self.get_max_data('duration')

        context['pie_label'], context['pie_data'] = self.get_pie_chart_data()
        context['series'], context['categories'] = self.get_line_plot_data()

        context['scatter_temp_data'] = self.get_scatter_plot_data('temp')
        context['scatter_rh_data'] = self.get_scatter_plot_data('humidity')
        context['scatter_thickness_data'] = self.get_scatter_plot_data('thickness')

        return context


class TableIceExpView(TemplateView):
    template_name = "icymelt/table-ice.html"

    def get_queryset(self):
        return IceExp.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ice_exp_list'] = self.get_queryset()
        return context


class TableMaterialView(TemplateView):
    template_name = "icymelt/table-material.html"

    def get_queryset(self):
        return Material.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['material'] = self.get_queryset()
        return context


class TableWeatherView(TemplateView):
    template_name = "icymelt/table-weather.html"

    def get_queryset(self):
        return WeatherCondition.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['weather'] = self.get_queryset()
        return context


class IceExpListCreate(generics.ListCreateAPIView):
    queryset = IceExp.objects.all()
    serializer_class = IceExpSerializer


class IceExpDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = IceExp.objects.all()
    serializer_class = IceExpSerializer
    lookup_field = 'pk'


class MaterialListCreate(generics.ListCreateAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class MaterialDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    lookup_field = 'pk'


class WeatherConditionListCreate(generics.ListCreateAPIView):
    queryset = WeatherCondition.objects.all()
    serializer_class = WeatherConditionSerializer


class WeatherConditionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = WeatherCondition.objects.all()
    serializer_class = WeatherConditionSerializer
    lookup_field = 'pk'


class ExperimentByMaterial(generics.ListAPIView):
    serializer_class = IceExpSerializer

    def get_queryset(self):
        mat_id = self.kwargs['mat_id']
        return IceExp.objects.filter(material_id=mat_id)


class ExperimentByWeatherCondition(generics.ListAPIView):
    serializer_class = IceExpSerializer

    def get_queryset(self):
        id = self.kwargs['id']
        return IceExp.objects.filter(weather_cond_id=id)


class ExperimentByMaterialAndWeatherCondition(generics.ListAPIView):
    serializer_class = IceExpSerializer

    def get_queryset(self):
        mat_id = self.kwargs['mat_id']
        wea_id = self.kwargs['wea_id']
        return IceExp.objects.filter(material_id=mat_id, weather_cond_id=wea_id)


class AverageAllMeasurements(APIView):
    def get(self, request):
        materials = IceExp.objects.values_list('material', flat=True).distinct()
        avg_data = {}

        for material_id in materials:
            material_data = IceExp.objects.filter(material=material_id).aggregate(
                avg_temp=Avg('temp'),
                avg_humidity=Avg('humidity'),
                avg_thickness=Avg('thickness'),
                avg_weight=Avg('weight'),
                avg_duration=Avg('duration')
            )
            record_count = IceExp.objects.filter(material=material_id).count()
            material_type = Material.objects.get(pk=material_id).type
            avg_data[material_id] = {
                'material_id': material_id,
                'material_type': material_type,
                'record_count': record_count,
                'temp': material_data['avg_temp'],
                'humidity': material_data['avg_humidity'],
                'thickness': material_data['avg_thickness'],
                'weight': material_data['avg_weight'],
                'duration': material_data['avg_duration']
            }

        return Response({'average': avg_data})


class TotalAllMeasurements(APIView):
    def get(self, request):
        materials = IceExp.objects.values_list('material', flat=True).distinct()
        total_data = {}

        for material_id in materials:
            material_data = IceExp.objects.filter(material=material_id).aggregate(
                total_temp=Sum('temp'),
                total_humidity=Sum('humidity'),
                total_thickness=Sum('thickness'),
                total_weight=Sum('weight'),
                total_duration=Sum('duration')
            )
            record_count = IceExp.objects.filter(material=material_id).count()
            material_type = Material.objects.get(pk=material_id).type
            total_data[material_id] = {
                'material_id': material_id,
                'material_type': material_type,
                'record_count': record_count,
                'temp': material_data['total_temp'],
                'humidity': material_data['total_humidity'],
                'thickness': material_data['total_thickness'],
                'weight': material_data['total_weight'],
                'duration': material_data['total_duration']
            }

        return Response({'total': total_data})


class MinAllMeasurements(APIView):
    def get(self, request):
        materials = IceExp.objects.values_list('material', flat=True).distinct()
        min_data = {}

        for material_id in materials:
            material_data = IceExp.objects.filter(material=material_id).aggregate(
                min_temp=Min('temp'),
                min_humidity=Min('humidity'),
                min_thickness=Min('thickness'),
                min_weight=Min('weight'),
                min_duration=Min('duration')
            )
            record_count = IceExp.objects.filter(material=material_id).count()
            material_type = Material.objects.get(pk=material_id).type
            min_data[material_id] = {
                'material_id': material_id,
                'material_type': material_type,
                'record_count': record_count,
                'temp': material_data['min_temp'],
                'humidity': material_data['min_humidity'],
                'thickness': material_data['min_thickness'],
                'weight': material_data['min_weight'],
                'duration': material_data['min_duration']
            }

        return Response({'min': min_data})


class MaxAllMeasurements(APIView):
    def get(self, request):
        materials = IceExp.objects.values_list('material', flat=True).distinct()
        max_data = {}

        for material_id in materials:
            material_data = IceExp.objects.filter(material=material_id).aggregate(
                max_temp=Max('temp'),
                max_humidity=Max('humidity'),
                max_thickness=Max('thickness'),
                max_weight=Max('weight'),
                max_duration=Max('duration')
            )
            record_count = IceExp.objects.filter(material=material_id).count()
            material_type = Material.objects.get(pk=material_id).type
            max_data[material_id] = {
                'material_id': material_id,
                'material_type': material_type,
                'record_count': record_count,
                'temp': material_data['max_temp'],
                'humidity': material_data['max_humidity'],
                'thickness': material_data['max_thickness'],
                'weight': material_data['max_weight'],
                'duration': material_data['max_duration']
            }

        return Response({'max': max_data})


class StatisticalAllMeasurements(APIView):
    def get(self, request):
        materials = IceExp.objects.values_list('material', flat=True).distinct()
        stats_data = {}

        for material_id in materials:
            material_data = IceExp.objects.filter(material=material_id).aggregate(
                avg_temp=Avg('temp'),
                min_temp=Min('temp'),
                max_temp=Max('temp'),
                total_temp=Sum('temp'),
                avg_humidity=Avg('humidity'),
                min_humidity=Min('humidity'),
                max_humidity=Max('humidity'),
                total_humidity=Sum('humidity'),
                avg_thickness=Avg('thickness'),
                min_thickness=Min('thickness'),
                max_thickness=Max('thickness'),
                total_thickness=Sum('thickness'),
                avg_weight=Avg('weight'),
                min_weight=Min('weight'),
                max_weight=Max('weight'),
                total_weight=Sum('weight'),
                avg_duration=Avg('duration'),
                min_duration=Min('duration'),
                max_duration=Max('duration'),
                total_duration=Sum('duration'),
            )
            record_count = IceExp.objects.filter(material=material_id).count()
            material_type = Material.objects.get(pk=material_id).type
            stats_data[material_id] = {
                'material_id': material_id,
                'material_type': material_type,
                'record_count': record_count,
                'temp': {
                    'mean': material_data['avg_temp'],
                    'min': material_data['min_temp'],
                    'max': material_data['max_temp'],
                    'total': material_data['total_temp']
                },
                'humidity': {
                    'mean': material_data['avg_humidity'],
                    'min': material_data['min_humidity'],
                    'max': material_data['max_humidity'],
                    'total': material_data['total_humidity']
                },
                'thickness': {
                    'mean': material_data['avg_thickness'],
                    'min': material_data['min_thickness'],
                    'max': material_data['max_thickness'],
                    'total': material_data['total_thickness']
                },
                'weight': {
                    'mean': material_data['avg_weight'],
                    'min': material_data['min_weight'],
                    'max': material_data['max_weight'],
                    'total': material_data['total_weight']
                },
                'duration': {
                    'mean': material_data['avg_duration'],
                    'min': material_data['min_duration'],
                    'max': material_data['max_duration'],
                    'total': material_data['total_duration']
                }
            }

        return Response(stats_data)


def get_api_paths(urlconf_module):
    resolver = get_resolver(urlconf_module)
    api_paths = {}

    # Get the URL patterns from the resolver
    url_patterns = resolver.url_patterns

    # Iterate over the URL patterns to find API paths
    for pattern in url_patterns:
        if hasattr(pattern, 'pattern'):
            # Access the pattern attribute to get the URLPattern object
            if pattern.name.endswith('_api'):
                url_pattern = pattern.pattern
                api_paths[pattern.name] = url_pattern

    return api_paths


def api_paths_view(request):
    api_paths = get_api_paths(urls)
    data = {
        "ice_exp_api": {"url": api_paths["ice_exp_api"], "description": "List all ice experiments"},
        "ice_exp_detail_api": {"url": api_paths["ice_exp_detail_api"], "description": "Retrieve an ice experiment with a specific id"},
        "experiment_by_material_api": {"url": api_paths["experiment_by_material_api"], "description": "List all ice experiments with a specific material"},
        "experiment_by_weather_condition_api": {"url": api_paths["experiment_by_weather_condition_api"], "description": "List all ice experiments with a specific weather condition"},
        "experiment_by_material_and_weather_condition_api": {"url": api_paths["experiment_by_material_and_weather_condition_api"], "description": "List all ice experiments with a specific material and weather condition"},
        "material_api": {"url": api_paths["material_api"], "description": "List all materials"},
        "material_detail_api": {"url": api_paths["material_detail_api"], "description": "Retrieve a material with a specific id"},
        "weather_api": {"url": api_paths["weather_api"], "description": "List all weather conditions"},
        "weather_condition_detail_api": {"url": api_paths["weather_condition_detail_api"], "description": "Retrieve a weather condition with a specific id"},
        "average_all_measurements_api": {"url": api_paths["average_all_measurements_api"], "description": "Get average values for all measurements"},
        "total_all_measurements_api": {"url": api_paths["total_all_measurements_api"], "description": "Get total values for all measurements"},
        "min_all_measurements_api": {"url": api_paths["min_all_measurements_api"], "description": "Get minimum values for all measurements"},
        "max_all_measurements_api": {"url": api_paths["max_all_measurements_api"], "description": "Get maximum values for all measurements"},
        "statistical_all_measurements_api": {"url": api_paths["statistical_all_measurements_api"], "description": "Get statistical values for all measurements"}
    }
    return render(request, 'icymelt/api_paths_template.html', {'api_paths': data})