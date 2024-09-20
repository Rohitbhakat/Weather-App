from datetime import datetime, timedelta

import requests
from django.conf import settings
from django.db.models import Avg
from django.utils import timezone

from .models import City, WeatherData


def fetch_cuurrent_data(city_name):
    api_url = f"{settings.CURRENT_WEATHER_URL}?key={settings.WEATHER_API_KEY}&q={city_name}&aqi=yes"

    response = requests.get(api_url)

    if response.status_code == 200:
        weather_info = response.json()

        return {
            "city_name": city_name,
            "temperature": weather_info["current"]["temp_c"],
            "humidity": weather_info["current"]["humidity"],
            "condition": weather_info["current"]["condition"]["text"],
            "wind_speed": weather_info["current"]["wind_kph"],
            "air_quality": weather_info["current"]["air_quality"],
        }
    else:
        raise Exception(
            f"Error fetching data for {city_name}: {response.status_code} - {response.text}"
        )


def fetch_historical_weather_data(city_name, date):
    weather_url = f"{settings.WEATHER_APP_URL}?key={settings.WEATHER_API_KEY}&q={city_name}&dt={date}"
    response = requests.get(weather_url)

    if response.status_code == 200:
        weather_data = response.json()
        return weather_data["forecast"]["forecastday"][0]["hour"]
    else:
        raise Exception(
            f"Error fetching data: {response.status_code} - {response.text}"
        )


def save_historical_weather_data(city_name, weather_info):
    city, _ = City.objects.get_or_create(name=city_name)

    for hour_data in weather_info:
        WeatherData.objects.create(
            city=city,
            temperature=hour_data["temp_c"],
            humidity=hour_data["humidity"],
            timestamp=datetime.strptime(hour_data["time"], "%Y-%m-%d %H:%M"),
        )


def get_24h_average(city_name):
    city = City.objects.get(name=city_name)
    last_24_hours = timezone.now() - timedelta(hours=24)

    avg_temp = WeatherData.objects.filter(
        city=city, timestamp__gte=last_24_hours
    ).aggregate(Avg("temperature"))["temperature__avg"]

    avg_humidity = WeatherData.objects.filter(
        city=city, timestamp__gte=last_24_hours
    ).aggregate(Avg("humidity"))["humidity__avg"]

    return {"average_temperature": avg_temp, "average_humidity": avg_humidity}


def check_extreme_weather(avg_weather):
    alert_message = None
    if avg_weather["average_temperature"] > 40:
        alert_message = "Extreme heat alert!"
    elif avg_weather["average_temperature"] < 0:
        alert_message = "Extreme cold alert!"
    return alert_message
