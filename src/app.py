from spots import load_spots
from api import get_swell, get_wind
from scoring import surf_score

def main():

    spots = load_spots()

    for spot in spots:
        lat = spot["lat"]
        lon = spot["lon"]

        swell_dict = get_swell(lat, lon)
        wind_dict = get_wind(lat, lon)

        swell_height = swell_dict["swell_wave_height"]
        swell_period = swell_dict["swell_wave_period"]
        swell_angle = swell_dict["swell_wave_direction"]
        wind_speed = wind_dict["wind_speed_10m"]
        wind_angle = wind_dict["wind_direction_10m"]
        beach_angle = spot["facing"]

        score = surf_score(swell_height, swell_period, swell_angle, wind_speed, wind_angle, beach_angle)

        print(f"{spot["name"]}: {score}")
        

main()

