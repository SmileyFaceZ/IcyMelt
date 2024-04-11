from django.views.generic import TemplateView
from icymelt.models import IceExp, Material, WeatherCondition
from django.db.models import Avg


class HomeView(TemplateView):
    template_name = "icymelt/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        avg_temp = IceExp.objects.all().aggregate(avg_temp=Avg('temp'))['avg_temp']
        context['avg_temp'] = round(avg_temp, 2)
        avg_rh = IceExp.objects.all().aggregate(avg_rh=Avg('humidity'))['avg_rh']
        context['avg_rh'] = round(avg_rh, 2)

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