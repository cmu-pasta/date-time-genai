
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timezone, timedelta
def time_elapsed_since_epoch(timestamp: datetime) -> timedelta:
    # Define the Unix epoch as a timezone-aware datetime in UTC
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    
    # Ensure the input timestamp is treated in UTC:
    # - If naive (no tzinfo), assume it's UTC.
    # - If aware, convert it to UTC.
    if timestamp.tzinfo is None:
        timestamp_utc = timestamp.replace(tzinfo=timezone.utc)
    else:
        timestamp_utc = timestamp.astimezone(timezone.utc)
    
    # Calculate and return the elapsed time since the epoch as a timedelta
    return timestamp_utc - epoch

# Entry point: time_elapsed_since_epoch(timestamp: datetime) -> timedelta

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_30_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_time_elapsed_since_epoch(timestamp):
    result = time_elapsed_since_epoch(timestamp)
    formatted_result = format_value_dt(result, timestamp)
    log_file.write(formatted_result + "\n")
