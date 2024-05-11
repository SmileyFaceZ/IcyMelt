from django.views.generic import TemplateView
from icymelt.models import IceExp, Material, WeatherCondition
from decimal import Decimal
from rest_framework import generics
from icymelt.serializers import IceExpSerializer, MaterialSerializer, WeatherConditionSerializer
from decouple import config
import requests
from collections import defaultdict, OrderedDict
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg, Sum, Min, Max, Count


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        avg_temp = IceExp.objects.all().aggregate(avg_temp=Avg('temp'))['avg_temp']
        context['avg_temp'] = round(avg_temp, 2)
        avg_rh = IceExp.objects.all().aggregate(avg_rh=Avg('humidity'))['avg_rh']
        context['avg_rh'] = round(avg_rh, 2)

        context['pie_label'], context['pie_data'] = self.get_pie_chart_data()
        context['series'], context['categories'] = self.get_line_plot_data()

        context['cur_temp'] = self.get_cur_temp()
        context['cur_rh'] = self.get_cur_rh()
        context['cur_condition'] = self.get_cur_condition()
        context['cur_wind'] = self.get_cur_wind()

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