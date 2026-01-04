from typing import Any
import requests
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)


def get_weather_data(latitude: float, longitude: float) -> dict[str, Any] | None:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,weather_code,is_day,relative_humidity_2m,wind_speed_10m",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min",
        "timezone": "auto",
    }

    try:
        response = requests.get(url, params=params, timeout=10.0)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Successfully fetched weather data for {latitude}, {longitude}")
        logger.info(f"Weather code: {data.get('current', {}).get('weather_code')}")
        return data
    except requests.RequestException as e:
        logger.error(f"Failed to fetch weather data: {e}")
        return None


def get_weather_theme(weather_code: int, is_day: bool) -> dict[str, str]:
    weather_type = "clear"
    if 0 <= weather_code <= 3:
        weather_type = "sunny"
    elif 45 <= weather_code <= 48:
        weather_type = "cloudy"
    elif 51 <= weather_code <= 67:
        weather_type = "rainy"
    elif 71 <= weather_code <= 77:
        weather_type = "snowy"
    elif 80 <= weather_code <= 82:
        weather_type = "rainy"
    elif 85 <= weather_code <= 86:
        weather_type = "snowy"
    elif 95 <= weather_code <= 99:
        weather_type = "rainy"

    themes = {
        "sunny": {
            "name": "Sunny",
            "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)",
            "card_bg": "rgba(255, 255, 255, 0.25)",
            "text_color": "#ffffff",
            "text_shadow": "0 2px 10px rgba(0, 0, 0, 0.1)",
            "icon_color": "#ffd700",
            "overlay": "radial-gradient(circle at 30% 20%, rgba(255, 200, 0, 0.4) 0%, transparent 50%)",
        },
        "cloudy": {
            "name": "Cloudy",
            "gradient": "linear-gradient(135deg, #3a4b5c 0%, #607d8b 50%, #7f8c8d 100%)",
            "card_bg": "rgba(255, 255, 255, 0.15)",
            "text_color": "#ffffff",
            "text_shadow": "0 2px 10px rgba(0, 0, 0, 0.2)",
            "icon_color": "#b0bec5",
            "overlay": "radial-gradient(circle at 70% 30%, rgba(100, 100, 100, 0.3) 0%, transparent 40%)",
        },
        "rainy": {
            "name": "Rainy",
            "gradient": "linear-gradient(135deg, #1a237e 0%, #311b92 50%, #4a148c 100%)",
            "card_bg": "rgba(255, 255, 255, 0.1)",
            "text_color": "#ffffff",
            "text_shadow": "0 2px 15px rgba(0, 0, 0, 0.3)",
            "icon_color": "#7c4dff",
            "overlay": "radial-gradient(circle at 50% 50%, rgba(60, 20, 100, 0.4) 0%, transparent 60%)",
        },
        "snowy": {
            "name": "Snowy",
            "gradient": "linear-gradient(135deg, #cfd9df 0%, #e2ebf0 50%, #ece9e6 100%)",
            "card_bg": "rgba(255, 255, 255, 0.6)",
            "text_color": "#2c3e50",
            "text_shadow": "0 2px 8px rgba(0, 0, 0, 0.1)",
            "icon_color": "#607d8b",
            "overlay": "radial-gradient(circle at 40% 60%, rgba(255, 255, 255, 0.5) 0%, transparent 50%)",
        },
    }

    return themes.get(weather_type, themes["sunny"])


def get_weather_icon(weather_code: int) -> str:
    if 0 <= weather_code <= 3:
        return "☀️"
    elif 45 <= weather_code <= 48:
        return "☁️"
    elif 51 <= weather_code <= 67:
        return "🌧️"
    elif 71 <= weather_code <= 77:
        return "❄️"
    elif 80 <= weather_code <= 82:
        return "🌦️"
    elif 85 <= weather_code <= 86:
        return "🌨️"
    elif 95 <= weather_code <= 99:
        return "⛈️"
    return "☀️"


def geocode_location(location: str) -> tuple[float, float] | None:
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": location, "count": 1, "language": "en", "format": "json"}

    try:
        response = requests.get(url, params=params, timeout=10.0)
        response.raise_for_status()
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]
            return result["latitude"], result["longitude"]
    except requests.RequestException as e:
        logger.error(f"Failed to geocode location: {e}")

    return None


@require_http_methods(["GET", "POST"])
def dashboard(request):
    location = request.GET.get("location", "London")
    weather_data = None
    theme = get_weather_theme(0, True)
    error = None

    if location:
        coords = geocode_location(location)
        if coords:
            latitude, longitude = coords
            weather_data = get_weather_data(latitude, longitude)

            if weather_data:
                current = weather_data.get("current", {})
                daily = weather_data.get("daily", {})

                weather_code = current.get("weather_code", 0)
                is_day = current.get("is_day", 1)

                logger.info(
                    f"Location: {location}, Weather code: {weather_code}, Theme: {get_weather_theme(weather_code, is_day)['name']}"
                )

                theme = get_weather_theme(weather_code, is_day)

                display_data = {
                    "location": location,
                    "city": location,
                    "current_temp": round(current.get("temperature_2m", 0)),
                    "weather_icon": get_weather_icon(weather_code),
                    "weather_type": theme["name"],
                    "humidity": f"{current.get('relative_humidity_2m', 50)}%",
                    "wind_speed": f"{current.get('wind_speed_10m', 0)} km/h",
                    "high_temp": round(daily.get("temperature_2m_max", [0])[0]),
                    "low_temp": round(daily.get("temperature_2m_min", [0])[0]),
                    "forecast": [],
                }

                for i in range(7):
                    day_code = daily.get("weather_code", [0])[i]
                    display_data["forecast"].append(
                        {
                            "day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][
                                (i + 1) % 7
                            ],
                            "high": round(daily.get("temperature_2m_max", [0])[i]),
                            "low": round(daily.get("temperature_2m_min", [0])[i]),
                            "icon": get_weather_icon(day_code),
                            "type": get_weather_theme(day_code, True)["name"],
                        }
                    )

                return render(
                    request,
                    "dashboard.html",
                    {"data": display_data, "theme": theme, "error": None},
                )
        else:
            error = "Location not found. Please try a different city name."
    else:
        error = "Please enter a city name."

    return render(
        request, "dashboard.html", {"data": None, "theme": theme, "error": error}
    )


def debug_view(request):
    test_codes = [
        {"code": 0, "name": "Clear sky", "theme": "sunny"},
        {"code": 1, "name": "Mainly clear", "theme": "sunny"},
        {"code": 45, "name": "Foggy", "theme": "cloudy"},
        {"code": 48, "name": "Depositing rime fog", "theme": "cloudy"},
        {"code": 51, "name": "Light drizzle", "theme": "rainy"},
        {"code": 61, "name": "Slight rain", "theme": "rainy"},
        {"code": 65, "name": "Heavy rain", "theme": "rainy"},
        {"code": 71, "name": "Slight snow fall", "theme": "snowy"},
        {"code": 77, "name": "Snow grains", "theme": "snowy"},
    ]

    test_data = []
    for test in test_codes:
        theme = get_weather_theme(test["code"], True)
        test_data.append(
            {
                "code": test["code"],
                "name": test["name"],
                "theme": theme,
                "icon": get_weather_icon(test["code"]),
            }
        )

    return render(request, "debug.html", {"test_data": test_data})
