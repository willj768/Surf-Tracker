import requests
from spots import load_spots
from api import get_forecast
from scoring import surf_score
from config import MODE
from db_handler import save_readings, init_db, upsert_spots, get_spot_ids

def main():
    init_db()
    upsert_spots()
    spot_ids = get_spot_ids()

    spots = load_spots()

    for spot in spots:
        try:
            surf_data = get_forecast(
                spot["lat"],
                spot["lon"],
                days=7
            )
        except (requests.RequestException, ValueError, KeyError) as e:
            print(f'Skipping {spot["name"]}: {e}')
            continue

        for reading in surf_data:
            inputs = (
                reading["swell_wave_height"],
                reading["swell_wave_period"],
                reading["swell_wave_direction"],
                reading["wind_speed_10m"],
                reading["wind_direction_10m"],
            )

            if None in inputs:
                reading["score"] = None
            else:
                reading["score"] = surf_score(*inputs, spot["facing"])

        if not surf_data:
            print(f'Skipping {spot["name"]}: no forecast data')
            continue

        save_readings(spot_ids[spot["name"]], surf_data, MODE)

if __name__ == "__main__":
    main()


