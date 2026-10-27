
import requests
from config import MARINE_URL, WIND_URL, MODE, TARGET_TIME

def get_forecast(lat, lon, days=7):
    marine_params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": (
            "swell_wave_height,"
            "swell_wave_period,"
            "swell_wave_direction"
        ),
        "forecast_days": days,
        "timezone": "Europe/London",
    }

    wind_params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "wind_speed_10m,wind_direction_10m",
        "forecast_days": days,
        "timezone": "Europe/London",
    }

    marine_response = requests.get(
        MARINE_URL, params=marine_params, timeout=10
    )
    marine_response.raise_for_status()
    marine = marine_response.json()["hourly"]

    wind_response = requests.get(
        WIND_URL, params=wind_params, timeout=10
    )
    wind_response.raise_for_status()
    wind = wind_response.json()["hourly"]

    wind_index = {
        time: i for i, time in enumerate(wind["time"])
    }

    readings = []

    for i, time in enumerate(marine["time"]):
        if time not in wind_index:
            continue

        j = wind_index[time]

        readings.append({
            "time": time,
            "swell_wave_height": marine["swell_wave_height"][i],
            "swell_wave_period": marine["swell_wave_period"][i],
            "swell_wave_direction": marine["swell_wave_direction"][i],
            "wind_speed_10m": wind["wind_speed_10m"][j],
            "wind_direction_10m": wind["wind_direction_10m"][j],
        })

    return readings

