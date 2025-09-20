
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def duration_milliseconds(ts1: datetime, ts2: datetime) -> float:
    """
    Calculate the duration in milliseconds between two timestamps.

    Args:
        ts1 (datetime): The first timestamp.
        ts2 (datetime): The second timestamp.

    Returns:
        float: The absolute duration between ts1 and ts2 in milliseconds.
    """
    delta = ts2 - ts1
    milliseconds = abs(delta.total_seconds() * 1000.0)
    return milliseconds

# Entry point: duration_milliseconds(ts1: datetime, ts2: datetime) -> float

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_36_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_duration_milliseconds(ts1, ts2):
    result = duration_milliseconds(ts1, ts2)
    formatted_result = format_value_dt(result, ts1, ts2)
    log_file.write(formatted_result + "\n")
