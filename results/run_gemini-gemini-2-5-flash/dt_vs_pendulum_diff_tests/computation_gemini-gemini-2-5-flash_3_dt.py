
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def _is_leap_year(year: int) -> bool:
    """
    Helper function to determine if a given year is a leap year.
    """
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def find_next_leap_year(start_date: datetime) -> int:
    """
    Determines the next leap year from or after a given date.

    Args:
        start_date: The datetime object from which to start the search.

    Returns:
        An integer representing the year of the next leap year.
    """
    current_year = start_date.year
    
    # Iterate from the current_year until a leap year is found
    while not _is_leap_year(current_year):
        current_year += 1
            
    return current_year

# Entry point: find_next_leap_year(start_date: datetime) -> integer

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_3_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_next_leap_year(start_date):
    result = find_next_leap_year(start_date)
    formatted_result = format_value_dt(result, start_date)
    log_file.write(formatted_result + "\n")
