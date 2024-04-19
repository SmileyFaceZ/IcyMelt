from django.views.generic import TemplateView
from icymelt.models import IceExp, Material, WeatherCondition
from django.db.models import Avg
from django.db.models import Count
from django.contrib.postgres.aggregates import ArrayAgg
from decimal import Decimal


class HomeView(TemplateView):
    template_name = "icymelt/home.html"

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

        series = []
        for entry in material_with_duration:
            _dict = {
                'name': str(Material.objects.get(id=entry['material'])),
                'data': [str(Decimal(str(value))) for value in
                         entry['duration_list']]
            }
            series.append(_dict)

        categories_obj = list(IceExp.objects.order_by('date').values_list('date', flat=True).distinct())
        categories = [date_obj.date() for date_obj in categories_obj]
        categories = [str(date) for date in categories]

        return series, categories

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        avg_temp = IceExp.objects.all().aggregate(avg_temp=Avg('temp'))['avg_temp']
        context['avg_temp'] = round(avg_temp, 2)
        avg_rh = IceExp.objects.all().aggregate(avg_rh=Avg('humidity'))['avg_rh']
        context['avg_rh'] = round(avg_rh, 2)

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
