import json
from config import JSON_PATH

def load_spots():
    with open(JSON_PATH) as f:
        spots = json.load(f)

    return spots
    
