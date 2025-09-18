
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time, datetime, date, timedelta
def minutes_since_midnight(t: time) -> int:
    """
    Convert a 24-hour time to minutes since midnight.

    If the time includes seconds or microseconds, this function floors to the nearest whole minute.
    """
    # Combine with an arbitrary date to create a datetime for precise difference
    dt = datetime.combine(date(2000, 1, 1), t)  # arbitrary fixed date
    midnight = datetime.combine(date(2000, 1, 1), time(0, 0))
    # Calculate total seconds since midnight and convert to whole minutes
    total_minutes = int((dt - midnight).total_seconds() // 60)
    return total_minutes

# Entry point: minutes_since_midnight(t: time) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_64txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy())
def test_minutes_since_midnight(t):
    result = minutes_since_midnight(t)
    formatted_result = format_value_dt(result, t)
    log_file.write(formatted_result + "\n")
