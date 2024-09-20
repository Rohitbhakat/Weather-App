from datetime import datetime

from django.shortcuts import render
from weather.services import (check_extreme_weather, fetch_cuurrent_data,
                              fetch_historical_weather_data, get_24h_average,
                              save_historical_weather_data)


def weather_form(request):
    return render(
        request,
        "weather_form.html",
    )


def get_weather_data(request, city_names):
    try:

        city_list = city_names.split(",")

        weather_data_list = []
        for city_name in city_list:
            city_name = city_name.strip()

            today = datetime.now().strftime("%Y-%m-%d")

            weather_info = fetch_historical_weather_data(city_name, today)

            save_historical_weather_data(city_name, weather_info)

            avg_weather = get_24h_average(city_name)

            alert_message = check_extreme_weather(avg_weather)

            weather_data_list.append(
                {
                    "city_name": city_name,
                    "average_temperature": avg_weather["average_temperature"],
                    "average_humidity": avg_weather["average_humidity"],
                    "alert": alert_message,
                }
            )

        return render(request, "historical_weather.html", {"weather_data_list": weather_data_list})
    except Exception as e:
        return render(request, "error.html", {"error_message": str(e)})


def get_current_weather(request, city_names):
    try:
        city_list = city_names.split(",")
        current_weather_data_list = []

        for city_name in city_list:
            city_name = city_name.strip()
            current_weather_data = fetch_cuurrent_data(city_name)

            current_weather_data_list.append(current_weather_data)

        return render(
            request,
            "current_weather.html",
            {"current_weather_data_list": current_weather_data_list},
        )

    except Exception as e:
        return render(request, "error.html", {"error_message": str(e)})
