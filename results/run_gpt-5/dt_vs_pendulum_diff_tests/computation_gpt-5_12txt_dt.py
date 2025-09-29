
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def calculate_week_number(d: date) -> int:
    """
    Calculate the ISO 8601 week number for a given date.

    Parameters:
    - d (date): The date for which to compute the week number.

    Returns:
    - int: The ISO week number (1-53).
    """
    # ISO 8601: weeks start on Monday; week 1 is the week with the year's first Thursday
    return d.isocalendar().week

# Entry point: calculate_week_number(d: date) -> int

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_12txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_calculate_week_number(d):
    result = calculate_week_number(d)
    formatted_result = format_value_dt(result, d)
    log_file.write(formatted_result + "\n")
