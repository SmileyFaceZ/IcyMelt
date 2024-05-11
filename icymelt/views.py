from django.views.generic import TemplateView
from icymelt.models import IceExp, Material, WeatherCondition
from django.db.models import Avg, Min, Max
from django.db.models import Count
from django.contrib.postgres.aggregates import ArrayAgg
from decimal import Decimal
from rest_framework import generics
from icymelt.serializers import IceExpSerializer
from decouple import config
import requests
from collections import defaultdict, OrderedDict


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


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print('data:', self.get_average_data('temp'))
        context['avg_temp'] = self.get_average_data('temp')
        context['min_temp'] = self.get_min_data('temp')
        context['max_temp'] = self.get_max_data('temp')

        context['avg_rh'] = self.get_average_data('humidity')
        context['min_rh'] = self.get_min_data('humidity')
        context['max_rh'] = self.get_max_data('humidity')

        context['pie_label'], context['pie_data'] = self.get_pie_chart_data()
        context['series'], context['categories'] = self.get_line_plot_data()

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


# [
#     {
#         'name': 'Wood',
#         'data': ['2235.00', '1512.00', '1990.00']
#     },
#     {
#         'name': 'Ground',
#         'data': ['517.00', '943.00', '676.00', '508.00', '437.00', '533.00', '329.00', '829.00', '713.00', '657.00', '439.00']}, {'name': 'Tile', 'data': ['905.00', '879.00', '773.00', '687.00', '868.00', '811.00', '876.00', '839.00', '556.00']}, {'name': 'Iron', 'data': ['245.00', '286.00', '350.00', '398.00', '271.00', '305.00', '230.00', '267.00', '288.00', '361.00']}, {'name': 'Plastic', 'data': ['1796.00']}]