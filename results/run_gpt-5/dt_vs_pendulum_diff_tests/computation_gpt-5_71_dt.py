
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def _julian_day_to_date(jd: float) -> date:
    # Converts Julian Day to Gregorian calendar date (no time), using standard algorithm.
    # This conversion uses the convention that JD starts at noon; adding 0.5 aligns to midnight.
    J = jd + 0.5
    Z = int(J)
    F = J - Z
    if Z < 2299161:
        A = Z
    else:
        alpha = int((Z - 1867216.25) / 36524.25)
        A = Z + 1 + alpha - alpha // 4
    B = A + 1524
    C = int((B - 122.1) / 365.25)
    D = int(365.25 * C)
    E = int((B - D) / 30.6001)
    # Day with fractional part; we only need the calendar date, so take integer day
    day_float = B - D - int(30.6001 * E) + F
    day = int(day_float)
    month = E - 1 if E < 14 else E - 13
    year = C - 4716 if month > 2 else C - 4715
    return date(year, month, day)

def find_vernal_equinox_date(year: int) -> date:
    """
    Compute the approximate date of the vernal (March) equinox for a given Gregorian year.
    Uses Meeus polynomial (valid and accurate to within about an hour for years ~1000–3000)
    to estimate the Julian Day of the equinox, then converts to a calendar date.
    Returns a datetime.date with the calendar day on which the equinox occurs (UTC).
    """
    # Meeus (Astronomical Algorithms) polynomial for March equinox (years 1000–3000)
    T = (year - 2000) / 1000.0
    jde = (
        2451623.80984
        + 365242.37404 * T
        + 0.05169 * (T ** 2)
        - 0.00411 * (T ** 3)
        - 0.00057 * (T ** 4)
    )
    # Convert Julian Day to Gregorian calendar date (UTC)
    return _julian_day_to_date(jde)

# Entry point: find_vernal_equinox_date(year: int) -> date

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_71_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_vernal_equinox_date(year):
    result = find_vernal_equinox_date(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
