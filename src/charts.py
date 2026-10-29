from db_handler import get_readings
from datetime import datetime
import io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def score_bar_chart(name):

    wanted_hours = {6, 18}

    results = get_readings(name)

    rows = results.get(name)
    
    if not rows:
        raise ValueError(f"No readings for {name}")
    
    filtered = [r for r in rows if datetime.fromisoformat(r["time"]).hour in wanted_hours and r["score"] is not None]

    formatted_time = [datetime.fromisoformat(r["time"]).strftime("%a %H:%M") for r in filtered]

    scores = [r["score"] for r in filtered]
    labels = formatted_time

    fig, ax = plt.subplots()

    ax.bar(labels, scores)
    ax.set_ylabel("Score (/100)")
    ax.set_ylim(0, 100)
    ax.set_title(name)
    ax.set_facecolor("none")

    colour="#2dd4bf"
    ax.bar(labels, scores, color=colour)

    ax.tick_params(colors="white")
    ax.tick_params(axis="x", labelrotation=90)

    ax.yaxis.label.set_color("white")
    ax.title.set_color("white")

    for spine in ax.spines.values():
        spine.set_color("white")

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", transparent=True)
    plt.close(fig)
    buf.seek(0)

    return buf
