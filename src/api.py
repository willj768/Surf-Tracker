import requests
from config import MARINE_URL, WIND_URL
from spots import load_spots

def get_swell(lat, lon):
    marine_params = {
        "latitude": lat,
        "longitude": lon,
        "current": "swell_wave_height,swell_wave_period,swell_wave_direction",
        "timezone": "Europe/London"
    }

    response = requests.get(MARINE_URL, params=marine_params, timeout=10)
    response.raise_for_status()
    return response.json()["current"]

def get_wind(lat, lon):
    wind_params = {
            "latitude": lat,
            "longitude": lon,
            "current": "wind_speed_10m,wind_direction_10m"
        }

    response = requests.get(WIND_URL, params=wind_params, timeout=10)
    response.raise_for_status()
    return response.json()["current"]


if __name__ == "__main__":
    spots = load_spots()

    for spot in spots:
        lat = spot["lat"]
        lon = spot["lon"]

        print(spot["name"])
        print(get_swell(lat, lon))
        print(get_wind(lat, lon))
    