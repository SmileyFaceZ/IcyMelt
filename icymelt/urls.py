from django.urls import path
from icymelt import views


appname = "icymelt"
urlpatterns = [
    path("", views.HomeView.as_view(), name='review'),
]
