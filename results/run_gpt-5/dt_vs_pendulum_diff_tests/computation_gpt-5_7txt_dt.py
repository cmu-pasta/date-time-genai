
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def is_leap_year(year: int) -> bool:
    """
    Determine if the given year is a leap year using the datetime library.
    
    Args:
        year (int): The year to check.
    
    Returns:
        bool: True if leap year, False otherwise.
    """
    try:
        # If February 29 exists for the given year, it's a leap year.
        date(year, 2, 29)
        return True
    except ValueError:
        # If creating Feb 29 raises an error, it's not a leap year.
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

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_7txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_is_leap_year(year):
    result = is_leap_year(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
