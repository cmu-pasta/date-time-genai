
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_nanoseconds_between(ts1: datetime, ts2: datetime) -> int:
    """
    Calculate the absolute number of nanoseconds between two datetime timestamps.
    """
    delta = ts2 - ts1  # type: ignore[arg-type]  # valid if both are datetime
    # Convert timedelta to nanoseconds using integer arithmetic:
    # total_ns = ((days * 86400) + seconds) * 1_000_000_000 + (microseconds * 1_000)
    total_ns = ((delta.days * 86_400) + delta.seconds) * 1_000_000_000 + (delta.microseconds * 1_000)
    return abs(total_ns)

# Entry point: calculate_nanoseconds_between(ts1: datetime, ts2: datetime) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_87txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_nanoseconds_between(ts1, ts2):
    result = calculate_nanoseconds_between(ts1, ts2)
    formatted_result = format_value_dt(result, ts1, ts2)
    log_file.write(formatted_result + "\n")
