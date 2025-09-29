
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def _normalize_longitude(lon: float) -> float:
    # Normalize longitude to the [-180, 180] range
    lon = (lon + 180.0) % 360.0 - 180.0
    return lon

def find_next_visible_eclipse(from_date: date, latitude: float, longitude: float) -> date:
    """
    Returns the date of the next solar eclipse approximately visible from the given location.
    Visibility is determined using coarse latitude/longitude bounding boxes for known future eclipses.
    Raises ValueError if no visible eclipse is found in the encoded catalog.
    """
    lat = latitude
    lon = _normalize_longitude(longitude)

    # Coarse catalog of future eclipses with very approximate visibility bounding boxes.
    # Each entry includes:
    # - 'd': eclipse date (UTC calendar date)
    # - 'boxes': a list of [min_lat, max_lat, min_lon, max_lon] boxes where visibility is likely
    # Notes: These are intentionally broad and simplified to avoid external dependencies.
    catalog = [
        # 2026 Aug 12 - Total (Greenland, Iceland, Spain; parts of Europe/N Atlantic)
        {"d": date(2026, 8, 12), "boxes": [
            [25.0, 75.0, -35.0, 30.0],   # W/C Europe, Iceland, N Atlantic
            [35.0, 70.0, -80.0, -40.0],  # Newfoundland/Labrador to Greenland fringe (partial)
        ]},
        # 2027 Aug 2 - Total (N Africa, Middle East)
        {"d": date(2027, 8, 2), "boxes": [
            [-5.0, 35.0, -20.0, 60.0],   # N Africa to Arabian Peninsula
        ]},
        # 2028 Jul 22 - Total (Australia, New Zealand)
        {"d": date(2028, 7, 22), "boxes": [
            [-50.0, -10.0, 110.0, 180.0],  # Australia to NZ and SW Pacific
        ]},
        # 2030 Jun 1 - Annular (Africa to Australia, broad partial elsewhere)
        {"d": date(2030, 6, 1), "boxes": [
            [-40.0, 20.0, 10.0, 150.0],   # Africa/Indian Ocean to Australia
        ]},
        # 2033 Mar 30 - Total (Alaska/Arctic/Far E Russia)
        {"d": date(2033, 3, 30), "boxes": [
            [50.0, 75.0, -170.0, -100.0],  # Alaska/Arctic Canada
            [50.0, 75.0, 120.0, 170.0],    # Far East Russia
        ]},
        # 2035 Sep 2 - Total (China, Korea, Japan)
        {"d": date(2035, 9, 2), "boxes": [
            [20.0, 50.0, 90.0, 150.0],   # E China to Japan
        ]},
        # 2044 Aug 23 - Total (W/N Canada; partial northern US)
        {"d": date(2044, 8, 23), "boxes": [
            [45.0, 70.0, -140.0, -60.0],  # Western to central Canada
        ]},
        # 2045 Aug 12 - Total (United States coast-to-coast; Caribbean)
        {"d": date(2045, 8, 12), "boxes": [
            [20.0, 45.0, -125.0, -70.0],  # Continental US band
            [10.0, 25.0, -90.0, -60.0],   # Caribbean vicinity (partial)
        ]},
        # 2048 Apr 1 - Annular (South America/Atlantic) - coarse
        {"d": date(2048, 4, 1), "boxes": [
            [-40.0, 10.0, -80.0, -30.0],  # Parts of S. America/Atlantic
        ]},
        # 2050 May 20 - Annular (Africa/Europe/Asia) - coarse
        {"d": date(2050, 5, 20), "boxes": [
            [0.0, 60.0, -10.0, 80.0],     # N Africa to E Europe/West Asia
        ]},
    ]

    # Find the earliest eclipse on/after from_date that covers the location
    for entry in catalog:
        d = entry["d"]
        if d < from_date:
            continue
        boxes = entry["boxes"]
        for b in boxes:
            min_lat, max_lat, min_lon, max_lon = b
            # Handle longitudes that might conceptually wrap across the dateline:
            if min_lon <= max_lon:
                lon_in = (lon >= min_lon) and (lon <= max_lon)
            else:
                # Wrapped interval, e.g., 170 to -170
                lon_in = (lon >= min_lon) or (lon <= max_lon)
            if (lat >= min_lat) and (lat <= max_lat) and lon_in:
                return d

    raise ValueError("No visible solar eclipse found in the available catalog after the given date.")

# Entry point: find_next_visible_eclipse(from_date: date, latitude: float, longitude: float) -> date

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_95_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), float_strategy(), float_strategy())
def test_find_next_visible_eclipse(from_date, latitude, longitude):
    result = find_next_visible_eclipse(from_date, latitude, longitude)
    formatted_result = format_value_dt(result, from_date, latitude, longitude)
    log_file.write(formatted_result + "\n")
