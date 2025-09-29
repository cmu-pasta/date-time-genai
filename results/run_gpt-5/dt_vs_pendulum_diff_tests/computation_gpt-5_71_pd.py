
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import math
import pendulum
def _march_equinox_jde(year: int) -> float:
    # Meeus, Astronomical Algorithms (approximation for March equinox)
    # Valid with good accuracy over many centuries; sufficient for date.
    T = (year - 2000) / 1000.0
    # Polynomial for the March equinox (JDE, Terrestrial Time)
    jde = (
        2451623.80984
        + 365242.37404 * T
        + 0.05169 * T * T
        - 0.00411 * T * T * T
        - 0.00057 * T * T * T * T
    )
    return jde

def _jd_to_utc_datetime(jd: float) -> pendulum.DateTime:
    # Convert Julian Day to Gregorian calendar date/time (UTC approximation).
    # We ignore the small TT-UTC difference; for determining the date this is fine.
    jd += 0.5
    Z = int(jd)
    F = jd - Z

    if Z >= 2299161:
        alpha = int((Z - 1867216.25) / 36524.25)
        A = Z + 1 + alpha - int(alpha / 4)
    else:
        A = Z

    B = A + 1524
    C = int((B - 122.1) / 365.25)
    D = int(365.25 * C)
    E = int((B - D) / 30.6001)

    day = B - D - int(30.6001 * E) + F
    month = E - 1 if E < 14 else E - 13
    year = C - 4716 if month > 2 else C - 4715

    # Time of day from fractional part
    day_int = int(day)
    frac = day - day_int
    total_seconds = frac * 86400.0

    hour = int(total_seconds // 3600)
    minute = int((total_seconds % 3600) // 60)
    second = int(round(total_seconds % 60))

    # Normalize any rounding overflow
    if second == 60:
        second = 0
        minute += 1
    if minute == 60:
        minute = 0
        hour += 1
    if hour == 24:
        hour = 0
        # Increment date by one day on overflow
        # Use pendulum to handle month/year transitions cleanly
        dt = pendulum.datetime(year, month, day_int, tz="UTC").add(days=1)
        return dt

    return pendulum.datetime(year, month, day_int, hour, minute, second, tz="UTC")

def vernal_equinox_date(year: int) -> pendulum.Date:
    # Compute the March equinox for the given year and return the calendar date (UTC).
    jde = _march_equinox_jde(year)
    dt_utc = _jd_to_utc_datetime(jde)
    return dt_utc.date()

# Entry point: vernal_equinox_date(year: int) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_71_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_vernal_equinox_date(year):
    result = vernal_equinox_date(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
