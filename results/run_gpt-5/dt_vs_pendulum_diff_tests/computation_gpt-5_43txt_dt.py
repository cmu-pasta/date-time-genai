
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def is_weekend(d: date) -> bool:
    """
    Determine if the given date falls on a weekend (Saturday or Sunday).
    
    Args:
        d: A datetime.date object representing the date to check.
    
    Returns:
        True if the date is Saturday or Sunday, otherwise False.
    """
    # Monday=0, Tuesday=1, ..., Saturday=5, Sunday=6
    return d.weekday() >= 5

# Entry point: is_weekend(d: date) -> bool

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_43txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_is_weekend(d):
    result = is_weekend(d)
    formatted_result = format_value_dt(result, d)
    log_file.write(formatted_result + "\n")
