import json

def load_spots():
    with open("data/surf_spots.json") as f:
        spots = json.load(f)

    return spots
    
