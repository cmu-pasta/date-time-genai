
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import math
import pendulum
def _solar_declination(dt: pendulum.DateTime) -> float:
    """
    Approximate solar declination (in radians) at a given UTC datetime using
    a standard Fourier series approximation in terms of the 'day angle' gamma.
    This is sufficiently accurate to identify the solstice date.
    """
    # Day of year (1..366)
    N = dt.day_of_year
    # Fractional hour
    hour = dt.hour + dt.minute / 60.0 + dt.second / 3600.0
    # Day angle (radians). Centered near solar noon to reduce bias.
    gamma = 2.0 * math.pi / 365.0 * ( (N - 1) + (hour - 12.0) / 24.0 )

    # Declination approximation (radians)
    delta = (
        0.006918
        - 0.399912 * math.cos(gamma)
        + 0.070257 * math.sin(gamma)
        - 0.006758 * math.cos(2.0 * gamma)
        + 0.000907 * math.sin(2.0 * gamma)
        - 0.002697 * math.cos(3.0 * gamma)
        + 0.001480 * math.sin(3.0 * gamma)
    )
    return delta

def winter_solstice_date(year: int) -> pendulum.Date:
    """
    Compute the UTC calendar date of the winter solstice for a given year.
    The solstice is identified as the instant when the solar declination
    reaches its minimum in UTC.

    Input:
      - year: integer year (e.g., 2025)

    Output:
      - pendulum.Date representing the UTC date on which the solstice occurs.
    """
    tz = pendulum.timezone("UTC")

    # Coarse search: hourly steps from Dec 20 00:00 to Dec 24 00:00 UTC
    start = pendulum.datetime(year, 12, 20, 0, 0, 0, tz=tz)
    end = pendulum.datetime(year, 12, 24, 0, 0, 0, tz=tz)

    best_dt = start
    best_decl = _solar_declination(start)

    dt = start
    while dt < end:
        decl = _solar_declination(dt)
        if decl < best_decl:
            best_decl = decl
            best_dt = dt
        dt = dt.add(hours=1)

    # Fine search: 5-minute steps in a ±12-hour window around the coarse minimum
    fine_start = best_dt.subtract(hours=12)
    fine_end = best_dt.add(hours=12)

    # Clamp to the original window to avoid year overflow
    if fine_start < start:
        fine_start = start
    if fine_end > end:
        fine_end = end

    dt = fine_start
    best_decl = _solar_declination(dt)
    best_dt = dt

    while dt <= fine_end:
        decl = _solar_declination(dt)
        if decl < best_decl:
            best_decl = decl
            best_dt = dt
        dt = dt.add(minutes=5)

    # Return the UTC date of the solstice moment
    return best_dt.date()

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_41_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_winter_solstice_date(year):
    result = winter_solstice_date(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
