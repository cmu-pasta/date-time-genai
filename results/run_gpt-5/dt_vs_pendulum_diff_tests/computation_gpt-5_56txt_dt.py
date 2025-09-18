
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def next_valentines_day(current: date) -> date:
    """
    Find the next Valentine's Day (February 14) strictly after the given date.
    
    Args:
        current: A date object representing the starting date.
    
    Returns:
        A date object representing the next Valentine's Day after 'current'.
    """
    valentines_this_year = date(current.year, 2, 14)
    if current < valentines_this_year:
        return valentines_this_year
    # If 'current' is on or after Feb 14 of this year, return next year's Feb 14
    return date(current.year + 1, 2, 14)

# Entry point: next_valentines_day(current: date) -> date

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_56txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_next_valentines_day(current):
    result = next_valentines_day(current)
    formatted_result = format_value_dt(result, current)
    log_file.write(formatted_result + "\n")
