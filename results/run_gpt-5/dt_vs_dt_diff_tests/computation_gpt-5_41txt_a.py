
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
import math
def find_winter_solstice_date(year: int) -> date:
    """
    Estimate the date of the winter (December) solstice for a given year.
    This uses a simple solar declination approximation and picks the date
    between December 20 and December 23 with the minimum declination.

    Input:
      - year: integer year (e.g., 2025)

    Output:
      - datetime.date representing the estimated winter solstice date (UTC-centric)
    """
    # Helper: compute approximate solar declination (degrees) for a given date
    # Using a common approximation: δ ≈ -23.44° * cos(360°/365 * (N + 10)),
    # where N is day index from Jan 1 (N=0 for Jan 1).
    def approx_declination(d: date) -> float:
        start_of_year = date(d.year, 1, 1)
        N = (d - start_of_year).days  # day index from Jan 1
        return -23.44 * math.cos(math.radians((360.0 / 365.0) * (N + 10)))

    # Consider common window for the December solstice
    candidates = [date(year, 12, day) for day in (20, 21, 22, 23)]

    # Select the date with the minimum (most negative) declination
    best = candidates[0]
    best_decl = approx_declination(best)
    for d in candidates[1:]:
        dec = approx_declination(d)
        if dec < best_decl:
            best_decl = dec
            best = d

    return best

# Entry point: find_winter_solstice_date(year: int) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_41txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_winter_solstice_date(year):
    result = find_winter_solstice_date(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
