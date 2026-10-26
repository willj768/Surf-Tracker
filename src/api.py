
import requests
from config import MARINE_URL, WIND_URL, MODE, TARGET_TIME


def get_surf_data(lat, lon, mode=MODE, target_time=TARGET_TIME):
    if mode == "current":
        marine_params = {
            "latitude": lat,
            "longitude": lon,
            "current": (
                "swell_wave_height,"
                "swell_wave_period,"
                "swell_wave_direction"
            ),
            "timezone": "Europe/London",
        }

        wind_params = {
            "latitude": lat,
            "longitude": lon,
            "current": "wind_speed_10m,wind_direction_10m",
            "timezone": "Europe/London",
        }

        marine_response = requests.get(
            MARINE_URL, params=marine_params, timeout=10
        )
        marine_response.raise_for_status()
        marine = marine_response.json()["current"]

        wind_response = requests.get(
            WIND_URL, params=wind_params, timeout=10
        )
        wind_response.raise_for_status()
        wind = wind_response.json()["current"]

        return {
            "time": marine["time"],
            "swell_wave_height": marine["swell_wave_height"],
            "swell_wave_period": marine["swell_wave_period"],
            "swell_wave_direction": marine["swell_wave_direction"],
            "wind_speed_10m": wind["wind_speed_10m"],
            "wind_direction_10m": wind["wind_direction_10m"],
        }

    elif mode == "forecast":
        marine_params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": (
                "swell_wave_height,"
                "swell_wave_period,"
                "swell_wave_direction"
            ),
            "forecast_days": 7,
            "timezone": "Europe/London",
        }

        wind_params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "wind_speed_10m,wind_direction_10m",
            "forecast_days": 7,
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

        if target_time not in marine["time"]:
            raise ValueError(f"No swell forecast for {target_time}")

        if target_time not in wind["time"]:
            raise ValueError(f"No wind forecast for {target_time}")

        i = marine["time"].index(target_time)
        j = wind["time"].index(target_time)

        return {
            "time": target_time,
            "swell_wave_height": marine["swell_wave_height"][i],
            "swell_wave_period": marine["swell_wave_period"][i],
            "swell_wave_direction": marine["swell_wave_direction"][i],
            "wind_speed_10m": wind["wind_speed_10m"][j],
            "wind_direction_10m": wind["wind_direction_10m"][j],
        }

    else:
        raise ValueError("mode must be 'current' or 'forecast'")
