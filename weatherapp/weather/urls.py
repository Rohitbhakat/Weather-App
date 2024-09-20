from django.urls import path
from . import views

urlpatterns = [
    path("", views.weather_form, name="weather_form"),
    path(
        "weather/average/<str:city_names>/",
        views.get_weather_data,
        name="get_weather_data",
    ),
    path(
        "weather/current/<str:city_names>/",
        views.get_current_weather,
        name="get_current_weather",
    ),
]
