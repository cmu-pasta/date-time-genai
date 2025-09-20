
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def _lon_in_range(lon: float, min_lon: float, max_lon: float) -> bool:
    """
    Check if a longitude falls within [min_lon, max_lon], handling wrap-around across the antimeridian.
    All longitudes are expected in the range [-180, 180].
    """
    # Normalize to [-180, 180]
    def norm(x: float) -> float:
        while x > 180:
            x -= 360
        while x < -180:
            x += 360
        return x

    lon = norm(lon)
    min_lon = norm(min_lon)
    max_lon = norm(max_lon)

    if min_lon <= max_lon:
        return min_lon <= lon <= max_lon
    # Wrapped interval (e.g., 170 to -170)
    return lon >= min_lon or lon <= max_lon

def _is_visible(lat: float, lon: float, min_lat: float, max_lat: float, min_lon: float, max_lon: float) -> bool:
    """
    Approximate visibility check using bounding boxes.
    """
    return (min_lat <= lat <= max_lat) and _lon_in_range(lon, min_lon, max_lon)

def find_next_visible_solar_eclipse(start: pendulum.Date, latitude: float, longitude: float) -> pendulum.Date:
    """
    Return the date of the next solar eclipse visible from the given location (latitude, longitude),
    strictly after the provided start date. If no eclipse in the internal catalog is visible from the
    location after the start date, return the date of the next eclipse after the start date regardless
    of visibility.

    Inputs:
      - start: pendulum.Date
      - latitude: float  (degrees, -90..90)
      - longitude: float (degrees, -180..180)

    Output:
      - pendulum.Date
    """
    # Internal catalog of selected upcoming eclipses with rough visibility bounding boxes.
    # Note: These are approximate and intended for demonstration purposes.
    eclipses = [
        # date, min_lat, max_lat, min_lon, max_lon
        (pendulum.date(2024, 4, 8),   15.0, 55.0,  -125.0,  -60.0),   # North America (total)
        (pendulum.date(2026, 8, 12),  25.0, 75.0,   -50.0,   30.0),   # Greenland, Iceland, Spain (total)
        (pendulum.date(2027, 8, 2),    5.0, 40.0,   -20.0,   60.0),   # N. Africa to Middle East (total)
        (pendulum.date(2028, 1, 26), -45.0, -10.0,  110.0,  155.0),   # Australia (annular)
        (pendulum.date(2030, 6, 1),   60.0, 85.0,  -160.0,   60.0),   # Arctic (annular)
        (pendulum.date(2031, 11, 14), -20.0, 20.0, -170.0, -120.0),   # Central Pacific (total, rough)
        (pendulum.date(2033, 3, 30),  55.0, 85.0,  -170.0,  -120.0),  # Alaska/Arctic (total)
        (pendulum.date(2035, 9, 2),   20.0, 50.0,   100.0,  150.0),   # China/Japan (total)
        (pendulum.date(2044, 8, 23),  45.0, 75.0,  -140.0,  -50.0),   # Canada (total)
        (pendulum.date(2045, 8, 12),  20.0, 45.0,  -125.0,  -70.0),   # USA (total)
    ]

    # Ensure we search in chronological order
    eclipses.sort(key=lambda row: row[0])

    next_any_after_start = None

    for date_obj, min_lat, max_lat, min_lon, max_lon in eclipses:
        if date_obj > start and next_any_after_start is None:
            next_any_after_start = date_obj
        if date_obj > start and _is_visible(latitude, longitude, min_lat, max_lat, min_lon, max_lon):
            return date_obj

    # Fallback: return the next eclipse after start (even if not visible) to satisfy return type.
    if next_any_after_start is not None:
        return next_any_after_start

    # If start is after our catalog, return the last known eclipse date as a conservative fallback.
    # This ensures a pendulum.Date is always returned.
    return eclipses[-1][0]

# Entry point: find_next_visible_solar_eclipse(start: pendulum.Date, latitude: float, longitude: float) -> pendulum.Date

def format_value_pd(*values):
    formatted_values = []

    for value in values:
        if isinstance(value, pendulum.DateTime):
            formatted_values.append(value.to_iso8601_string()[:-1])
        elif isinstance(value, pendulum.Date):
            formatted_values.append(value.to_date_string())
        elif isinstance(value, pendulum.Time):
            # Format time in the same way as datetime.time.isoformat() does
            formatted_time = (
                str(value.hour).zfill(2)
                + ":"
                + str(value.minute).zfill(2)
                + ":"
                + str(value.second).zfill(2)
            )
            if value.microsecond:
                # Padding microseconds to 6 digits
                formatted_time += "." + str(value.microsecond).zfill(6)
            formatted_values.append(formatted_time)
        elif isinstance(value, pendulum.Duration):
            formatted_values.append(str(value.total_seconds()))
        else:
            formatted_values.append(str(value))

    return ", ".join(formatted_values)

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_95_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), float_strategy(), float_strategy())
def test_find_next_visible_solar_eclipse(start, latitude, longitude):
    result = find_next_visible_solar_eclipse(start, latitude, longitude)
    formatted_result = format_value_pd(result, start, latitude, longitude)
    log_file.write(formatted_result + "\n")
