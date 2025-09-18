
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timezone, timedelta
def time_since_epoch(ts: datetime) -> timedelta:
    """
    Calculate the time elapsed since the Unix epoch (1970-01-01 00:00:00 UTC)
    for a given timestamp.

    - If the input datetime is timezone-aware, it will be converted to UTC.
    - If the input datetime is naive (no tzinfo), it is assumed to be in UTC.

    Returns:
        A timedelta representing the elapsed time since the epoch.
        This value can be negative for timestamps before the epoch.
    """
    # Step 1: Normalize to UTC
    if ts.tzinfo is None:
        ts_utc = ts.replace(tzinfo=timezone.utc)
    else:
        ts_utc = ts.astimezone(timezone.utc)

    # Step 2: Define the Unix epoch in UTC
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)

    # Step 3: Compute the elapsed time as a timedelta
    elapsed = ts_utc - epoch
    return elapsed

# Entry point: time_since_epoch(ts: datetime) -> timedelta

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_30txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_time_since_epoch(ts):
    result = time_since_epoch(ts)
    formatted_result = format_value_dt(result, ts)
    log_file.write(formatted_result + "\n")
