
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import math
import pendulum
def _jde_december_solstice(year: int) -> float:
    # Meeus, Astronomical Algorithms (Chapter 27)
    # T in thousands of years from J2000.0
    T = (year - 2000) / 1000.0

    # Base polynomial for December solstice (JDE0)
    JDE0 = (
        2451900.05952
        + 365242.74049 * T
        - 0.06223 * (T ** 2)
        - 0.00823 * (T ** 3)
        + 0.00032 * (T ** 4)
    )

    # Periodic terms (A, B, C) with angles in degrees
    A_vals = [
        485, 203, 199, 182, 156, 136, 77, 74, 70, 58, 52, 50,
        45, 44, 29, 18, 17, 16, 16, 15, 12, 12, 12, 12
    ]
    B_vals = [
        324.96, 337.23, 342.08, 27.85, 73.14, 171.52, 222.54, 296.72,
        243.58, 119.81, 297.17, 21.02, 247.54, 325.15, 60.93, 155.12,
        288.79, 198.04, 199.76, 95.39, 287.11, 320.81, 227.73, 15.45
    ]
    C_vals = [
        1934.136, 32964.467, 20.186, 445267.112, 45036.886, 22518.443,
        65928.934, 3034.906, 9037.513, 33718.147, 150.678, 2281.226,
        29929.562, 31555.956, 4443.417, 67555.328, 4562.452, 62894.029,
        31436.921, 14577.848, 31931.756, 34777.259, 1222.114, 16859.074
    ]

    # Sum of periodic correction terms
    S = 0.0
    i = 0
    # Using a simple loop to avoid complex outputs while keeping internal clarity
    while i < 24:
        angle_deg = B_vals[i] + C_vals[i] * T
        S += A_vals[i] * math.cos(math.radians(angle_deg))
        i += 1

    # Apply correction (units of days)
    JDE = JDE0 + 0.00001 * S
    return JDE

def _pendulum_datetime_from_jd_utc(jd: float) -> pendulum.DateTime:
    # Convert Julian Day (UTC) to Unix timestamp (seconds since 1970-01-01 00:00:00 UTC)
    unix_seconds = (jd - 2440587.5) * 86400.0
    # Create a pendulum DateTime in UTC
    return pendulum.from_timestamp(unix_seconds, tz="UTC")

def winter_solstice_date(year: int) -> pendulum.Date:
    """
    Approximate date of the Northern Hemisphere winter solstice for a given year.
    The computation yields the UTC date of the solstice instant (approximate).
    """
    # Compute JDE for December solstice and approximate UTC as TT ≈ UTC for date purposes
    jde = _jde_december_solstice(year)
    dt_utc = _pendulum_datetime_from_jd_utc(jde)
    # Return only the calendar date (pendulum.Date)
    return dt_utc.date()

# Entry point: winter_solstice_date(year: int) -> pendulum.Date

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_41txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_winter_solstice_date(year):
    result = winter_solstice_date(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
