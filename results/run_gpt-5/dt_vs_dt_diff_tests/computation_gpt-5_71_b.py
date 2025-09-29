
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def vernal_equinox_date(year: int) -> date:
    # Step 1: Compute the approximate Julian Ephemeris Day (JDE) for the March equinox (Meeus polynomial)
    # T is in Julian centuries from J2000.0
    T = (year - 2000) / 100.0
    JDE = (
        2451623.80984
        + 365242.37404 * T
        + 0.05169 * (T ** 2)
        - 0.00411 * (T ** 3)
        - 0.00057 * (T ** 4)
    )
    # Step 2: Approximate UT by TT for date extraction (Delta T ignored for date-level resolution)
    JD = JDE  # Using JD ≈ JDE for determining the calendar date

    # Step 3: Convert Julian Day to Gregorian calendar date (Fliegel–Van Flandern style conversion)
    # We convert JD to an integer Julian Day Number at midnight by adding 0.5 then flooring.
    JDN = int(JD + 0.5)

    # Integer-based conversion
    L = JDN + 68569
    N = (4 * L) // 146097
    L = L - (146097 * N + 3) // 4
    I = (4000 * (L + 1)) // 1461001
    L = L - (1461 * I) // 4 + 31
    J = (80 * L) // 2447
    day = L - (2447 * J) // 80
    L = J // 11
    month = J + 2 - 12 * L
    year_g = 100 * (N - 49) + I + L

    # Step 4: Return as a date object
    return date(int(year_g), int(month), int(day))

# Entry point: vernal_equinox_date(year: int) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_71_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_vernal_equinox_date(year):
    result = vernal_equinox_date(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
