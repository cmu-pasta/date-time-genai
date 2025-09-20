
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def is_leap_year(year: int) -> bool:
    """
    Determines if a given year is a leap year using the datetime library.

    A year is a leap year if it is divisible by 4, unless it is divisible by 100
    but not by 400. This function infers leap year status by checking if
    February 29th exists in that year.

    Args:
        year: An integer representing the year.

    Returns:
        True if the year is a leap year, False otherwise.
    """
    try:
        # Attempt to create a datetime object for February 29th of the given year.
        # If this date exists, the year is a leap year.
        datetime(year, 2, 29)
        return True
    except ValueError:
        # If a ValueError is raised (e.g., "day is out of range for month"),
        # it means February 29th does not exist in that year, so it's not a leap year.
        return False

# Entry point: is_leap_year(year: int) -> bool

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_7_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_is_leap_year(year):
    result = is_leap_year(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
