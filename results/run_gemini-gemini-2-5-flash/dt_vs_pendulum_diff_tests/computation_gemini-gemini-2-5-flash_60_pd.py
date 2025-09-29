
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
import math
def calculate_solar_noon(date: pendulum.Date, latitude: float, longitude: float) -> pendulum.DateTime:
    """
    Calculates the solar noon time for a given date and location coordinates.

    This implementation uses a simplified set of astronomical formulas.
    Solar noon is the moment when the Sun crosses the local meridian and
    reaches its highest point in the sky.

    Args:
        date (pendulum.Date): The date for which to calculate solar noon.
        latitude (float): The latitude of the location in degrees.
        longitude (float): The longitude of the location in degrees.

    Returns:
        pendulum.DateTime: A pendulum.DateTime object representing the solar noon
                           at the specified location on the given date, in UTC.
    """
    # 1. Day of the year (N)
    N = date.day_of_year

    # 2. Fractional year (gamma) in radians
    gamma = (2 * math.pi / 365) * (N - 1)

    # 3. Equation of Time components (in minutes)
    # C1, C2, C3 are coefficients derived from astronomical approximations
    eqtime_minutes = (
        229.18 * (
            0.000075 +
            0.001868 * math.cos(gamma) - 0.032077 * math.sin(gamma) -
            0.014615 * math.cos(2 * gamma) - 0.040849 * math.sin(2 * gamma)
        )
    )

    # 4. Time Correction Factor (TC) in minutes
    # This combines the equation of time and the longitude correction.
    # The '4 * longitude' part accounts for 4 minutes of time per degree of longitude.
    time_correction_minutes = 4 * longitude + eqtime_minutes

    # 5. Base UTC noon for the given date
    # Start with 12:00:00 UTC for the given date.
    base_utc_noon = pendulum.datetime(date.year, date.month, date.day, 12, 0, 0, tz='UTC')

    # 6. Apply the time correction to find solar noon
    # The time_correction_minutes is how much earlier or later than 12:00:00 local mean time
    # the solar noon occurs, adjusted for longitude.
    # A positive time_correction_minutes means solar noon is later than 12:00 UTC,
    # a negative means it's earlier.
    solar_noon_utc = base_utc_noon.add(minutes=time_correction_minutes)

    return solar_noon_utc

# Entry point: calculate_solar_noon(date: pendulum.Date, latitude: float, longitude: float) -> pendulum.DateTime

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_60_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), float_strategy(), float_strategy())
def test_calculate_solar_noon(date, latitude, longitude):
    result = calculate_solar_noon(date, latitude, longitude)
    formatted_result = format_value_pd(result, date, latitude, longitude)
    log_file.write(formatted_result + "\n")
