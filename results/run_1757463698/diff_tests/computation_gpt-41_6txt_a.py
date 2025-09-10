
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timezone
def seconds_since_unix_epoch(dt: datetime) -> float:
    # Step 1: Ensure datetime is aware and in UTC
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    
    # Step 2: Define the UNIX epoch (1970-01-01T00:00:00Z)
    unix_epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    
    # Step 3: Compute the difference between the input datetime and epoch
    delta = dt - unix_epoch
    
    # Step 4: Get the total number of seconds (including fractions)
    seconds = delta.total_seconds()
    
    # Step 5: Return the result
    return seconds

# Entry point: seconds_since_unix_epoch(dt: datetime) -> float

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_6txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_seconds_since_unix_epoch(dt):
    result = seconds_since_unix_epoch(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
