from pathlib import Path

MARINE_URL = "https://marine-api.open-meteo.com/v1/marine"
WIND_URL = "https://api.open-meteo.com/v1/forecast"

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
JSON_PATH = DATA_DIR / "surf_spots.json"
DB_PATH = DATA_DIR / "surf.db"

DEBUG_SPOTS = ("Croyde", "Saunton", "Sennen", "Fistral", "Praa Sands")

LOW_PERIOD_BOUNDARY = 6
HIGH_PERIOD_BOUNDARY = 12

LOW_HEIGHT_BOUNDARY = 0.3

IDEAL_HEIGHT = 1.25
HIGH_HEIGHT_BOUNDARY = 2.5

LOW_SWELL_DIRECTION_BOUNDARY = 20
HIGH_SWELL_DIRECTION_BOUNDARY = 70

HEIGHT_WEIGHT = 0.22
PERIOD_WEIGHT = 0.25
SWELL_DIRECTION_WEIGHT = 0.2
WIND_WEIGHT = 0.33

MIN_SUB_SCORE = 0.005

#API Settings
MODE = "forecast" #current or forecast
TARGET_TIME = "2026-11-01T09:00"