from spots import load_spots
from api import get_surf_data
from scoring import surf_score

def main():

    spots = load_spots()

    total_score = 0

    for spot in spots:
        lat = spot["lat"]
        lon = spot["lon"]

        surf_data = get_surf_data(lat, lon)

        swell_height = surf_data["swell_wave_height"]
        swell_period = surf_data["swell_wave_period"]
        swell_angle = surf_data["swell_wave_direction"]
        wind_speed = surf_data["wind_speed_10m"]
        wind_angle = surf_data["wind_direction_10m"]
        beach_angle = spot["facing"]

        score = surf_score(swell_height, swell_period, swell_angle, wind_speed, wind_angle, beach_angle)
        
        total_score += score

        if spot["name"] in ("Croyde", "Saunton", "Sennen", "Fistral", "Praa Sands"):
            print(f'{spot["name"]} ({spot["facing"]}): {score}')
            print(surf_data)

    print(f"Average: {total_score / 19}")
        

main()

