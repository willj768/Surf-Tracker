from db_handler import get_readings
import matplotlib.pyplot as plt
from datetime import datetime

def score_bar_chart(name):

    wanted_hours = {6, 18}

    results = get_readings(name)
    rows = results[name]
    filtered = [r for r in rows if datetime.fromisoformat(r["time"]).hour in wanted_hours]

    formatted_time = [datetime.fromisoformat(r["time"]).strftime("%a %d\n%H:%M") for r in filtered]

    scores = [r["score"] for r in filtered]
    labels = formatted_time
    plt.bar(labels, scores)
    plt.ylabel("Score (/100)")
    plt.ylim(0, 100)
    plt.title(name)
    plt.show()
