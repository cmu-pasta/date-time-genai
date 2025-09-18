
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def days_since_reference(dt: datetime, reference: datetime) -> int:
    """
    Convert a datetime to the number of days since a reference datetime.
    The calculation uses calendar days by comparing the date components.
    
    Args:
        dt: The target datetime.
        reference: The reference datetime to measure from.
    
    Returns:
        Integer number of days between the date of dt and the date of reference.
        Positive if dt is after reference, negative if before, zero if same date.
    """
    # Use date components to compute whole-day differences irrespective of time-of-day
    days_difference = (dt.date() - reference.date()).days
    return days_difference

# Entry point: days_since_reference(dt: datetime, reference: datetime) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_76txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_days_since_reference(dt, reference):
    result = days_since_reference(dt, reference)
    formatted_result = format_value_dt(result, dt, reference)
    log_file.write(formatted_result + "\n")
