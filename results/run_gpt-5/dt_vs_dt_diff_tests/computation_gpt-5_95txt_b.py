
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def _in_box(lat: float, lon: float, lat_min: float, lat_max: float, lon_min: float, lon_max: float) -> bool:
    # Checks if a point (lat, lon) lies within the inclusive bounding box
    return (lat_min <= lat <= lat_max) and (lon_min <= lon <= lon_max)

def find_next_visible_solar_eclipse(from_date: date, latitude: float, longitude: float) -> date:
    # Simplified visibility catalog: coarse bounding boxes where the eclipse is (at least partial) visible.
    # Note: These are approximate and intended for demonstration, not precise astronomical prediction.
    eclipses = [
        # 2026 Aug 12: Broad visibility across North America and Europe (approximate partial visibility region)
        {"d": date(2026, 8, 12), "lat_min": -5.0,  "lat_max": 85.0, "lon_min": -170.0, "lon_max": 60.0},
        # 2027 Aug 02: North Africa, southern Europe, Middle East (approximate)
        {"d": date(2027, 8, 2),  "lat_min": -40.0, "lat_max": 50.0, "lon_min": -20.0,  "lon_max": 60.0},
        # 2028 Jan 26: Australia and parts of SE Asia (approximate)
        {"d": date(2028, 1, 26), "lat_min": -50.0, "lat_max": 20.0, "lon_min": 80.0,   "lon_max": 180.0},
        # 2030 Jun 01: Arctic/Asia regions (approximate)
        {"d": date(2030, 6, 1),  "lat_min": 20.0,  "lat_max": 85.0, "lon_min": 30.0,   "lon_max": 180.0},
        # 2035 Sep 02: East Asia (approximate)
        {"d": date(2035, 9, 2),  "lat_min": 0.0,   "lat_max": 70.0, "lon_min": 90.0,   "lon_max": 180.0},
        # 2044 Aug 23: North America (approximate)
        {"d": date(2044, 8, 23), "lat_min": 20.0,  "lat_max": 85.0, "lon_min": -170.0, "lon_max": -30.0},
        # 2045 Aug 12: North America (approximate)
        {"d": date(2045, 8, 12), "lat_min": 10.0,  "lat_max": 80.0, "lon_min": -170.0, "lon_max": -30.0},
    ]

    # Ensure chronological order
    eclipses.sort(key=lambda e: e["d"])

    # Find the next eclipse strictly after from_date that is visible from (latitude, longitude)
    for e in eclipses:
        if e["d"] > from_date and _in_box(latitude, longitude, e["lat_min"], e["lat_max"], e["lon_min"], e["lon_max"]):
            return e["d"]

    # If none found in the catalog, return a sentinel maximum date
    return date.max

# Entry point: find_next_visible_solar_eclipse(from_date: date, latitude: float, longitude: float) -> date

def format_value_dt(*values):
    formatted_values = []

    for value in values:
        if isinstance(value, datetime):
            formatted_values.append(value.isoformat())
        elif isinstance(value, date):
            # Use strftime to format the date similar to to_date_string()
            formatted_values.append(value.strftime("%Y-%m-%d"))
        elif isinstance(value, time):
            formatted_values.append(value.isoformat())
        elif isinstance(value, timedelta):
            formatted_values.append(str(value.total_seconds()))
        else:
            formatted_values.append(str(value))

    return ", ".join(formatted_values)

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_95txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), float_strategy(), float_strategy())
def test_find_next_visible_solar_eclipse(from_date, latitude, longitude):
    result = find_next_visible_solar_eclipse(from_date, latitude, longitude)
    formatted_result = format_value_dt(result, from_date, latitude, longitude)
    log_file.write(formatted_result + "\n")
