import sqlite3
from config import DB_PATH, JSON_PATH
from datetime import datetime
import json

def get_connection():

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    return conn

def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS spots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            coast TEXT NOT NULL,
            lat REAL NOT NULL,
            lon REAL NOT NULL,
            facing INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            spot_id INTEGER NOT NULL REFERENCES spots(id),
            time TEXT NOT NULL,
            fetched_at TEXT NOT NULL,
            mode TEXT NOT NULL,
            swell_height REAL,
            swell_period REAL,
            swell_direction REAL,
            wind_speed REAL,      -- km/h
            wind_direction REAL,
            score INTEGER,
            UNIQUE (spot_id, time, fetched_at)
        );
    """)

    conn.commit()
    conn.close()

def save_readings(spot_id, surf_data, mode):
    conn = get_connection()
    cursor = conn.cursor()

    fetched_at = datetime.now().isoformat(timespec="minutes")

    try:

        cursor.execute("""
            DELETE FROM readings
            WHERE spot_id = ? AND mode = ?
        """, (spot_id, mode))

        for reading in surf_data:
            cursor.execute("""
                INSERT OR IGNORE INTO readings (
                    spot_id, time, fetched_at, mode,
                    swell_height, swell_period, swell_direction,
                    wind_speed, wind_direction, score
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                spot_id,
                reading["time"],
                fetched_at,
                mode,
                reading["swell_wave_height"],
                reading["swell_wave_period"],
                reading["swell_wave_direction"],
                reading["wind_speed_10m"],
                reading["wind_direction_10m"],
                reading["score"]
            ))

        clear_readings(cursor)
        conn.commit()

    finally:
        conn.close()


def upsert_spots():
    
    conn = get_connection()
    cursor = conn.cursor()

    with open(JSON_PATH) as f:
        spots = json.load(f)

    cursor.executemany("""
            INSERT INTO spots (name, coast, lat, lon, facing)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                coast = excluded.coast,
                lat = excluded.lat,
                lon = excluded.lon,
                facing = excluded.facing
        """, [
            (
                spot["name"],
                spot["coast"],
                spot["lat"],
                spot["lon"],
                spot["facing"]
            )
            for spot in spots
        ])

    conn.commit()
    conn.close()

def get_spot_ids():
    conn = get_connection()
    rows = conn.execute("SELECT id, name FROM spots").fetchall()
    conn.close()

    return {row["name"]: row["id"] for row in rows}

def clear_readings(cursor):
    cursor.execute("""
        DELETE FROM readings
        WHERE datetime(time) < datetime('now', 'localtime')
    """)

def get_reading(spot_name, forecast_time):

    conn = get_connection()
    try:
        row = conn.execute("""
            SELECT
                r.swell_height,
                r.swell_period,
                r.swell_direction,
                r.wind_speed,
                r.wind_direction,
                s.facing,
                s.name
            FROM readings r
            JOIN spots s ON s.id = r.spot_id
            WHERE s.name = ? AND r.time = ?
            ORDER BY r.fetched_at DESC
            LIMIT 1
        """, (spot_name, forecast_time)).fetchone()

    finally:
        conn.close()

    return row
