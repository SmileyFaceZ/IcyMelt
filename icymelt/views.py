from django.views.generic import TemplateView
from icymelt.models import IceExp, Material, WeatherCondition
from django.db.models import Avg
from django.db.models import Count
from django.contrib.postgres.aggregates import ArrayAgg
from decimal import Decimal
from rest_framework import generics
from icymelt.serializers import IceExpSerializer
from decouple import config
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

    @staticmethod
    def get_line_plot_data():
        material_with_duration = IceExp.objects.values('material').annotate(
            duration_list=ArrayAgg('duration')
        )
        print("material_with_duration: ", material_with_duration)
        series = []
        for entry in material_with_duration:
            _dict = {
                'name': str(Material.objects.get(id=entry['material'])),
                'data': [str(Decimal(str(value))) for value in
                         entry['duration_list']]
            }
            series.append(_dict)
        print("series: ", series, len(series))

        categories_obj = list(IceExp.objects.order_by('date').values_list('date', flat=True).distinct())
        print('='*100)
        categories = [dt.strftime('%Y-%m-%d %H:%M:%S') for dt in categories_obj]
        print("categories: ", categories, len(categories))


        # categories = ['2024-05-04 11:08', '2024-05-04 11:09', '2024-05-04 11:10', '2024-05-04 11:11', '2024-05-04 11:12', '2024-05-04 11:13', '2024-05-04 11:14', '2024-05-04 11:15', '2024-05-04 11:16', '2024-05-04 11:17', '2024-05-04 11:18']
        # series = [
        #     {'name': 'Wood', 'data': ['2235.00', '0', '0', '0', '0', '0', '2000']},
        #     {'name': 'Ground', 'data': ['517.00', '943.00', '676.00', '508.00', '437.00', '533.00', '329.00', '829.00', '713.00', '657.00', '439.00']},
        #     {'name': 'Tile', 'data': ['905.00', '879.00', '773.00', '687.00', '868.00', '811.00', '876.00', '839.00', '556.00']},
        #     {'name': 'Iron', 'data': ['245.00', '286.00', '350.00', '398.00', '271.00', '305.00', '230.00', '267.00', '288.00', '361.00']},
        #     {'name': 'Plastic', 'data': ['1796.00']}
        # ]

        # date_list = list(
        #     IceExp.objects.order_by('date').values_list('date',
        #                                                 flat=True).distinct())
        # date_list = [dt.date() for dt in date_list]
        # print("date_list: ", date_list)
        # aaa = IceExp.objects.filter(material=1)
        # print("objects: ", aaa)
        # for i in aaa:
        #     print("i: ", i.date)
        #
        # for date in date_list:
        #     ice_exp_objects = IceExp.objects.filter(date=date)
        #     print("ice_exp_objects: ", ice_exp_objects)


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


# [
#     {
#         'name': 'Wood',
#         'data': ['2235.00', '1512.00', '1990.00']
#     },
#     {
#         'name': 'Ground',
#         'data': ['517.00', '943.00', '676.00', '508.00', '437.00', '533.00', '329.00', '829.00', '713.00', '657.00', '439.00']}, {'name': 'Tile', 'data': ['905.00', '879.00', '773.00', '687.00', '868.00', '811.00', '876.00', '839.00', '556.00']}, {'name': 'Iron', 'data': ['245.00', '286.00', '350.00', '398.00', '271.00', '305.00', '230.00', '267.00', '288.00', '361.00']}, {'name': 'Plastic', 'data': ['1796.00']}]