
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date
def days_since_reference(dt: datetime, reference: date) -> int:
    """
    Convert a datetime to the number of whole days since a reference date.

    Parameters:
    - dt: A datetime object representing the target moment.
    - reference: A date object representing the reference (start) date.

    Returns:
    - An integer representing the number of days between dt's calendar date and the reference date.
      The result can be negative if dt is before the reference.
    """
    # Align to date granularity by taking the calendar date component of the datetime
    dt_as_date: date = dt.date()

    # Compute the difference in days
    delta = dt_as_date - reference

    # Return the integer day count
    return delta.days

# Entry point: days_since_reference(dt: datetime, reference: date) -> int

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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_76txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), date_strategy())
def test_days_since_reference(dt, reference):
    result = days_since_reference(dt, reference)
    formatted_result = format_value_dt(result, dt, reference)
    log_file.write(formatted_result + "\n")
