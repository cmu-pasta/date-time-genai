
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date, time, timedelta
def total_minutes_between(start: time, end: time) -> int:
    """
    Calculate the total whole minutes in the time period between two times.
    If end is earlier than start, the period is assumed to cross midnight into the next day.

    Args:
        start (time): The starting time.
        end (time): The ending time.

    Returns:
        int: The total number of whole minutes between start and end.
    """
    reference_day = date(1900, 1, 1)
    start_dt = datetime.combine(reference_day, start)
    end_dt = datetime.combine(reference_day, end)

    if end_dt < start_dt:
        end_dt += timedelta(days=1)

    delta = end_dt - start_dt
    total_minutes = int(delta.total_seconds() // 60)
    return total_minutes

# Entry point: total_minutes_between(start: time, end: time) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_51txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy(), time_strategy())
def test_total_minutes_between(start, end):
    result = total_minutes_between(start, end)
    formatted_result = format_value_dt(result, start, end)
    log_file.write(formatted_result + "\n")
