from django.urls import path
from icymelt import views


app_name = "icymelt"
urlpatterns = [
    path("", views.HomeView.as_view(), name='home'),
    path("ice-experiment/", views.TableIceExpView.as_view(), name='ice_exp'),
    path("material/", views.TableMaterialView.as_view(), name='material'),
    path("weather/", views.TableWeatherView.as_view(), name='weather'),
    path("api/experiments/", views.IceExpListCreate.as_view(), name="ice_exp_api"),
    path("api/experiment/<int:pk>/", views.IceExpDetail.as_view(), name="ice_exp_detail_api"),
    # path("api/experiment/material/<id>", views.MaterialListCreate.as_view(), name="all_experiment_material_api"),
    path("api/materials/", views.MaterialListCreate.as_view(), name="material_api"),
    path("api/material/<int:pk>/", views.MaterialDetail.as_view(), name="material_detail_api"),
    path("api/weather-conditions/", views.WeatherConditionListCreate.as_view(), name="weather_api"),
    path("api/weather-condition/<int:pk>/", views.WeatherConditionDetail.as_view(), name="weather_condition_detail_api"),
]
