from django.urls import path
from icymelt import views


app_name = "icymelt"
urlpatterns = [
    path("", views.HomeView.as_view(), name='home'),
    path("ice-experiment/", views.TableIceExpView.as_view(), name='ice_exp'),
    path("material/", views.TableMaterialView.as_view(), name='material'),
    path("weather/", views.TableWeatherView.as_view(), name='weather'),
    path("api/ice-exp/", views.IceExpListCreate.as_view(), name="ice_exp_api"),
    path("api/ice-exp/<int:pk>/", views.IceExpDetail.as_view(), name="ice_exp_detail_api"),
]
