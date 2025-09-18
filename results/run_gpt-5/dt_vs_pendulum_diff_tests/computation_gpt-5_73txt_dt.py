
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time
def is_within_business_hours(t: time) -> bool:
    """
    Determine if a given time falls within business hours: 09:00:00 (inclusive) to 17:00:00 (exclusive).
    The comparison respects tzinfo: if the input time has tzinfo, the bounds are created with the same tzinfo.
    """
    # Define business hour bounds, aligned with the input time's tzinfo if present
    start = time(9, 0, 0, tzinfo=t.tzinfo) if t.tzinfo else time(9, 0, 0)
    end = time(17, 0, 0, tzinfo=t.tzinfo) if t.tzinfo else time(17, 0, 0)
    
    # Check if the time is within [09:00:00, 17:00:00)
    return start <= t < end

# Entry point: is_within_business_hours(t: time) -> bool

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_73txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy())
def test_is_within_business_hours(t):
    result = is_within_business_hours(t)
    formatted_result = format_value_dt(result, t)
    log_file.write(formatted_result + "\n")
