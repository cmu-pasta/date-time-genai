
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, time, timedelta
def total_minutes_between_times(t1: time, t2: time) -> float:
    """
    Calculate the total minutes in the time period between two times.
    If t2 is earlier than t1, the period is assumed to cross midnight into the next day.

    Args:
        t1 (time): Start time.
        t2 (time): End time.

    Returns:
        float: Total minutes between t1 and t2.
    """
    # Step 1: Use a reference date to combine with the times
    ref_date = datetime(1900, 1, 1)
    dt1 = datetime.combine(ref_date.date(), t1)
    dt2 = datetime.combine(ref_date.date(), t2)

    # Step 2: Handle crossing midnight
    if dt2 < dt1:
        dt2 += timedelta(days=1)

    # Step 3: Compute the difference and convert to minutes
    delta = dt2 - dt1
    minutes = delta.total_seconds() / 60.0
    return float(minutes)

# Entry point: total_minutes_between_times(t1: time, t2: time) -> float

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_51txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy(), time_strategy())
def test_total_minutes_between_times(t1, t2):
    result = total_minutes_between_times(t1, t2)
    formatted_result = format_value_dt(result, t1, t2)
    log_file.write(formatted_result + "\n")
