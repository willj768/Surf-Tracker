import requests
import json
from spots import load_spots
from api import get_forecast
from scoring import surf_score
from config import MODE, JSON_PATH, HTML_PATH, STATIC_DIR
from db_handler import save_readings, init_db, upsert_spots, get_spot_ids, get_readings
from charts import score_bar_chart
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

with open(JSON_PATH) as f:
    spots = json.load(f)
    names = [spot["name"] for spot in spots]

@app.get("/")
def home():
    return FileResponse(HTML_PATH)

@app.get("/search")
def search(q: str):

    if not q.strip():
        return []

    q = q.lower()

    filtered_list = [name for name in names if q in name.lower()]

    return filtered_list[:8]

@app.get("/readings/{spot_name}")
def readings(spot_name: str):
    results = get_readings(spot_name)
    return results

@app.get("/chart/{spot_name}")
def chart(spot_name: str):
    try:
        buf = score_bar_chart(spot_name)
    except ValueError:
        raise HTTPException(status_code=404, detail="No readings for this spot")
    return Response(content=buf.getvalue(), media_type="image/png")


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

    score_bar_chart("Porthleven")

if __name__ == "__main__":
    main()


