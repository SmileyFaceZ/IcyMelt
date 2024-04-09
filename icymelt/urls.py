from django.urls import path
from icymelt import views


app_name = "icymelt"
urlpatterns = [
    path("", views.HomeView.as_view(), name='home'),
    path("table/", views.TableView.as_view(), name='table'),
]
