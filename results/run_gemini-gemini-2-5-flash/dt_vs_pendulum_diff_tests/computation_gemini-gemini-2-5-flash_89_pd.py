
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_nowruz_date(year: int) -> pendulum.Date:
    """
    Finds the approximate date of the Persian New Year (Nowruz) for a given Gregorian year.
    
    NOTE: Pendulum does not provide astronomical calculations for the precise
    vernal equinox. This implementation uses a common approximation where Nowruz
    is assumed to be March 20th for most years in the Gregorian calendar,
    as this is the most frequent date for the spring equinox.
    A truly precise calculation would require external astronomical libraries
    or complex algorithms.

    Args:
        year (int): The Gregorian year.

    Returns:
        pendulum.Date: A pendulum.Date object representing the approximate date of Nowruz.
    """
    # Step 1: Nowruz typically falls on March 20th or 21st, coinciding with the
    # vernal equinox. Without astronomical calculation capabilities in Pendulum,
    # we use the most common date for the spring equinox.
    # For many years, especially in the 21st century, March 20th is the day.
    
    # Step 2: Create a pendulum.Date object for March 20th of the given year.
    nowruz_date = pendulum.date(year, 3, 20)
    
    # While a precise calculation would involve checking the exact equinox time
    # relative to Tehran's noon, this is not possible with Pendulum alone.
    # Therefore, this function provides the most common approximate date.

    return nowruz_date

# Entry point: find_nowruz_date(year: int) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_89_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_nowruz_date(year):
    result = find_nowruz_date(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
