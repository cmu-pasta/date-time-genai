
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def next_visible_solar_eclipse(start: date, latitude: float, longitude: float) -> date:
    # Normalize longitude to [-180, 180]
    lon = ((longitude + 180.0) % 360.0) - 180.0
    lat = latitude

    # Simplified dataset of upcoming solar eclipses and approximate visibility bounding boxes.
    # Each entry: (eclipse_date, [(min_lat, max_lat, min_lon, max_lon), ...])
    # Note: These are coarse approximations intended for demonstration, not precise predictions.
    eclipses = [
        # 2026-08-12 Total: Greenland, Iceland, northern Spain (approx)
        (date(2026, 8, 12), [
            (35.0, 45.0, -10.0,   5.0),   # Spain/Portugal area (coarse)
            (63.0, 67.0, -25.0, -13.0),   # Iceland (coarse)
            (60.0, 85.0, -60.0, -20.0),   # Greenland (coarse)
        ]),
        # 2027-08-02 Total: North Africa, Egypt, Arabian Peninsula (approx)
        (date(2027, 8, 2), [
            (5.0, 35.0, -20.0,  55.0),    # North Africa to Arabian Peninsula (coarse)
        ]),
        # 2028-07-22 Total: Australia (approx)
        (date(2028, 7, 22), [
            (-45.0, -10.0, 110.0, 160.0), # Australia region (coarse)
        ]),
        # 2033-03-30 Total: Alaska / Far East Russia (approx; includes wrap-around near dateline)
        (date(2033, 3, 30), [
            (55.0, 75.0, -170.0, -140.0), # Alaska
            (55.0, 75.0,  160.0,  180.0), # Far East Russia near 180E
        ]),
        # 2035-09-02 Total: China / Japan (approx)
        (date(2035, 9, 2), [
            (25.0, 45.0, 110.0, 145.0),   # Eastern China to Japan (coarse)
        ]),
    ]

    # Ensure we consider eclipses on or after the start date
    for e_date, regions in eclipses:
        if e_date < start:
            continue
        # Check if location falls within any bounding box
        for (min_lat, max_lat, min_lon, max_lon) in regions:
            # Handle standard box
            if min_lon <= max_lon:
                if (lat >= min_lat and lat <= max_lat and lon >= min_lon and lon <= max_lon):
                    return e_date
            else:
                # Handle wrap-around boxes (not used above, but kept for completeness)
                in_lon = (lon >= min_lon) or (lon <= max_lon)
                if (lat >= min_lat and lat <= max_lat and in_lon):
                    return e_date

    raise ValueError("No known upcoming solar eclipse visible from the given location in the dataset.")

# Entry point: next_visible_solar_eclipse(start: date, latitude: float, longitude: float) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_95_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), float_strategy(), float_strategy())
def test_next_visible_solar_eclipse(start, latitude, longitude):
    result = next_visible_solar_eclipse(start, latitude, longitude)
    formatted_result = format_value_dt(result, start, latitude, longitude)
    log_file.write(formatted_result + "\n")
