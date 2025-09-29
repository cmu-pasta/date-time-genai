
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def _jde0_march_equinox(year: int) -> float:
    """
    Compute the approximate Julian Ephemeris Day (JDE0) for the March equinox
    using the polynomial from Meeus' Astronomical Algorithms (valid for years
    roughly between 1000 and 3000). This approximation is sufficient to obtain
    the correct calendar date in most practical cases.
    """
    T = (year - 2000) / 1000.0
    # JDE0 for March equinox
    return (
        2451623.80984
        + 365242.37404 * T
        + 0.05169 * (T ** 2)
        - 0.00411 * (T ** 3)
        - 0.00057 * (T ** 4)
    )

def _jd_to_gregorian_date(jd: float) -> pendulum.Date:
    """
    Convert Julian Day to a Gregorian calendar date (UTC date).
    This uses the standard algorithm and returns only the calendar date
    by effectively evaluating the civil date corresponding to JD.
    """
    # Shift because Julian Day starts at noon
    Z = int(jd + 0.5)
    F = (jd + 0.5) - Z

    if Z >= 2299161:
        alpha = int((Z - 1867216.25) / 36524.25)
        A = Z + 1 + alpha - int(alpha / 4)
    else:
        A = Z

    B = A + 1524
    C = int((B - 122.1) / 365.25)
    D = int(365.25 * C)
    E = int((B - D) / 30.6001)

    day_float = B - D - int(30.6001 * E) + F
    # Integer calendar day
    day = int(day_float)

    if E < 14:
        month = E - 1
    else:
        month = E - 13

    if month > 2:
        year = C - 4716
    else:
        year = C - 4715

    return pendulum.date(year, month, day)

def find_vernal_equinox(year: int) -> pendulum.Date:
    """
    Compute and return the UTC calendar date of the vernal (March) equinox
    for the given Gregorian year using an approximate astronomical formula.
    Output type is pendulum.Date.
    """
    jde0 = _jde0_march_equinox(year)
    # Convert JDE to (UTC) civil date; for date purposes, TT vs UTC difference is negligible
    date_utc = _jd_to_gregorian_date(jde0)
    return date_utc

# Entry point: find_vernal_equinox(year: int) -> pendulum.Date

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

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_71txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_vernal_equinox(year):
    result = find_vernal_equinox(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
