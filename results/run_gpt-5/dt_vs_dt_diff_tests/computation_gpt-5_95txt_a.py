
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def next_visible_solar_eclipse(latitude: float, longitude: float, start_from: date) -> date:
    """
    Returns the date of the next solar eclipse approximately visible from the given location
    on or after the provided start date.

    Notes:
    - This implementation uses coarse geographic bounding boxes for visibility approximation.
    - The dataset includes a subset of upcoming eclipses with broad visibility regions.
    - If no eclipse in the dataset is visible from the location after start_from, returns date.max.
    """

    # Helper: check if a point is inside a latitude/longitude box
    def _in_box(lat: float, lon: float, lat_min: float, lat_max: float, lon_min: float, lon_max: float) -> bool:
        return (lat_min <= lat <= lat_max) and (lon_min <= lon <= lon_max)

    # Helper: check if a point is within any of a collection of boxes
    def _visible_in_any_box(lat: float, lon: float, boxes: tuple) -> bool:
        # boxes is a tuple of (lat_min, lat_max, lon_min, lon_max)
        for b in boxes:
            if _in_box(lat, lon, b[0], b[1], b[2], b[3]):
                return True
        return False

    # Coarse visibility regions for selected upcoming eclipses (post-2025).
    # Dates are in ISO (YYYY, M, D). Boxes are broad approximations for partial/total visibility.
    # Sources: public eclipse path summaries; regions intentionally generous to capture likely visibility.
    eclipses = (
        # 2026-08-12 Total (Greenland, Iceland, Spain); partial across much of Europe and N Africa.
        # Broad region: Europe and North Africa
        (date(2026, 8, 12), (
            # Europe (broad)
            (35.0, 71.0, -25.0, 40.0),
            # Iceland
            (63.0, 67.0, -25.0, -12.0),
            # Greenland (south to mid)
            (60.0, 75.0, -74.0, -10.0),
            # Iberian Peninsula emphasis
            (36.0, 44.0, -9.8, 3.8),
        )),
        # 2027-08-02 Total (North Africa, Middle East); partial across N Africa, S Europe, Arabian Peninsula.
        (date(2027, 8, 2), (
            # North Africa and Middle East broad band
            (10.0, 36.0, -17.0, 55.0),
            # Southern Europe fringe
            (35.0, 47.0, -10.0, 30.0),
        )),
        # 2028-07-22 Total (Australia, New Zealand); partial across Australia/NZ and nearby regions.
        (date(2028, 7, 22), (
            # Australia
            (-44.0, -11.0, 113.0, 154.0),
            # New Zealand
            (-47.0, -34.0, 166.0, 179.9),
            # Nearby Indonesia/Timor-Leste fringe
            (-11.0, 6.0, 115.0, 141.0),
        )),
    )

    # Ensure longitude is within [-180, 180] for box comparisons
    lon = longitude
    if lon > 180.0:
        lon = ((lon + 180.0) % 360.0) - 180.0
    elif lon < -180.0:
        lon = ((lon - 180.0) % 360.0) + 180.0

    # Iterate chronologically and return the first eclipse visible from the location
    for e_date, e_boxes in eclipses:
        if e_date >= start_from and _visible_in_any_box(latitude, lon, e_boxes):
            return e_date

    # If none found in our dataset, return a sentinel extreme date
    return date.max

# Entry point: next_visible_solar_eclipse(latitude: float, longitude: float, start_from: date) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_95txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(float_strategy(), float_strategy(), date_strategy())
def test_next_visible_solar_eclipse(latitude, longitude, start_from):
    result = next_visible_solar_eclipse(latitude, longitude, start_from)
    formatted_result = format_value_dt(result, latitude, longitude, start_from)
    log_file.write(formatted_result + "\n")
