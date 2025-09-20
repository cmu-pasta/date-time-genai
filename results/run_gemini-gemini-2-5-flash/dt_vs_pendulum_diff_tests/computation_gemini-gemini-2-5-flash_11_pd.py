
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_easter_sunday(year: int) -> pendulum.Date:
    """
    Calculates the date of Easter Sunday for a given year using the Anonymous Gregorian algorithm.
    This algorithm is valid for years after 1582.

    Args:
        year (int): The year for which to calculate Easter Sunday.

    Returns:
        pendulum.Date: A pendulum.Date object representing Easter Sunday for the given year.
    """
    # Step 1: Anonymous Gregorian algorithm to calculate Easter Sunday
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    
    # Calculate month (1 = January, ..., 12 = December)
    easter_month = (h + l - 7 * m + 114) // 31
    
    # Calculate day
    easter_day = ((h + l - 7 * m + 114) % 31) + 1
    
    # Step 2: Construct and return the pendulum.Date object
    return pendulum.date(year, easter_month, easter_day)

# Entry point: find_easter_sunday(year: int) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_11_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_easter_sunday(year):
    result = find_easter_sunday(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
