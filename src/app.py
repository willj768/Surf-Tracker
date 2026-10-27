import requests
from spots import load_spots
from api import get_forecast
from scoring import score_reading
from config import MODE
from db_handler import save_readings, init_db, upsert_spots, get_spot_ids

def main():
    init_db()
    upsert_spots()
    spot_ids = get_spot_ids()

    spots = load_spots()

    total_score = 0
    scored = 0

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

        if not surf_data:
            print(f'Skipping {spot["name"]}: no forecast data')
            continue

        save_readings(spot_ids[spot["name"]], surf_data, MODE)

        current = surf_data[0]

        swell_height = current["swell_wave_height"]
        swell_period = current["swell_wave_period"]
        swell_angle = current["swell_wave_direction"]
        wind_speed = current["wind_speed_10m"]
        wind_angle = current["wind_direction_10m"]
        beach_angle = spot["facing"]

        if None in (
            swell_height,
            swell_period,
            swell_angle,
            wind_speed,
            wind_angle
        ):
            print(f'Skipping {spot["name"]}: missing data')
            continue

    score = score_reading("Fistral", "2026-11-01T11:00")
    
    if score is not None:
        print(f"Surf Score: {score}")

if __name__ == "__main__":
    main()


