from django.views.generic import TemplateView
from django.http import HttpResponse


class HomeView(TemplateView):
    template_name = "icymelt/home.html"

    def get_context_data(self, **kwargs):
        return


class TableView(TemplateView):
    template_name = "icymelt/table.html"

    def get_context_data(self, **kwargs):
        return