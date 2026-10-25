import requests
import json
from config import MARINE_URL, WIND_URL
from spots import load_spots

def get_swell(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "swell_wave_height,swell_wave_period,swell_wave_direction",
        "timezone": "Europe/London",
    }
    response = requests.get(MARINE_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()["current"]

spots = load_spots()

for spot in spots:
    lat = spot["lat"]
    lon = spot["lon"]

    print(spot["name"])
    print(get_swell(lat, lon))
    