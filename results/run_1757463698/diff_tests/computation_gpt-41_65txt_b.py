
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timezone
def datetime_to_filetime(dt: datetime) -> int:
    # Step 1: Define the FILETIME epoch (Jan 1, 1601, 00:00:00 UTC)
    FILETIME_EPOCH = datetime(1601, 1, 1, tzinfo=timezone.utc)

    # Step 2: Ensure the input datetime is UTC
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)

    # Step 3: Calculate the timedelta since FILETIME epoch
    delta = dt - FILETIME_EPOCH

    # Step 4: Calculate total 100-nanosecond intervals
    filetime = delta.days * 24 * 60 * 60 * 10_000_000
    filetime += delta.seconds * 10_000_000
    filetime += delta.microseconds * 10

    # Step 5: Return the result as an integer
    return filetime

# Entry point: datetime_to_filetime(dt: datetime) -> int

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

if not os.path.exists(".logs/diff_test_logs"):
    os.makedirs(".logs/diff_test_logs")
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_65txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_datetime_to_filetime(dt):
    result = datetime_to_filetime(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
