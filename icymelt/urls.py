from django.urls import path
from icymelt import views


app_name = "icymelt"
urlpatterns = [
    path("", views.HomeView.as_view(), name='home'),
    path("ice-experiment/", views.TableIceExpView.as_view(), name='ice_exp'),
    path("material/", views.TableMaterialView.as_view(), name='material'),
    path("weather/", views.TableWeatherView.as_view(), name='weather'),
    path('api/', views.api_paths_view, name='api_paths'),
    path("api/experiments/", views.IceExpListCreate.as_view(), name="ice_exp_api"),
    path("api/experiment/<int:id>/", views.IceExpDetail.as_view(), name="ice_exp_detail_api"),
    path("api/materials/", views.MaterialListCreate.as_view(), name="material_api"),
    path("api/material/<int:id>/", views.MaterialDetail.as_view(), name="material_detail_api"),
    path("api/weather-conditions/", views.WeatherConditionListCreate.as_view(), name="weather_api"),
    path("api/weather-condition/<int:id>/", views.WeatherConditionDetail.as_view(), name="weather_condition_detail_api"),
    path("api/experiment/material/<int:mat_id>/", views.ExperimentByMaterial.as_view(),
         name="experiment_by_material_api"),
    path("api/experiment/weather-condition/<int:id>/", views.ExperimentByWeatherCondition.as_view(),
         name="experiment_by_weather_condition_api"),
    path("api/experiment/material/<int:mat_id>/weather-condition/<int:wea_id>/",
         views.ExperimentByMaterialAndWeatherCondition.as_view(),
         name="experiment_by_material_and_weather_condition_api"),
    path("api/averageAllMeasurements/", views.AverageAllMeasurements.as_view(), name="average_all_measurements_api"),
    path("api/totalAllMeasurements/", views.TotalAllMeasurements.as_view(), name="total_all_measurements_api"),
    path("api/minAllMeasurements/", views.MinAllMeasurements.as_view(), name="min_all_measurements_api"),
    path("api/maxAllMeasurements/", views.MaxAllMeasurements.as_view(), name="max_all_measurements_api"),
    path("api/statisticalAllMeasurements/", views.StatisticalAllMeasurements.as_view(),
         name="statistical_all_measurements_api"),
]
