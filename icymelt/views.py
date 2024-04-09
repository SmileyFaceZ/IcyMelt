from django.views.generic import TemplateView
from django.http import HttpResponse


class HomeView(TemplateView):
    template_name = "icymelt/home.html"

    # def get(self, request, *args, **kwargs):
    #     return HttpResponse("Hello, world. You're at the icymelt index.")

    def get_context_data(self, **kwargs):
        return