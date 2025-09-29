
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timezone, timedelta
def calculate_elapsed_since_epoch(timestamp: datetime) -> float:
    # Step 1: Define the Unix epoch (January 1, 1970, 00:00:00 UTC)
    # It's crucial for the epoch to be timezone-aware (UTC).
    epoch_utc = datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

    # Step 2: Ensure the input timestamp is timezone-aware and in UTC
    if timestamp.tzinfo is None:
        # If the input timestamp is naive, assume it's UTC for epoch calculation
        # and attach the UTC timezone.
        processed_timestamp = timestamp.replace(tzinfo=timezone.utc)
    else:
        # If the timestamp is already timezone-aware, convert it to UTC
        processed_timestamp = timestamp.astimezone(timezone.utc)
    
    # Step 3: Calculate the difference (time elapsed)
    # The result of subtracting two datetime objects is a timedelta object.
    time_elapsed: timedelta = processed_timestamp - epoch_utc
    
    # Step 4: Extract the total number of seconds from the timedelta
    # total_seconds() returns the difference in seconds as a float.
    return time_elapsed.total_seconds()

# Entry point: calculate_elapsed_since_epoch(timestamp: datetime) -> float

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_30_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_elapsed_since_epoch(timestamp):
    result = calculate_elapsed_since_epoch(timestamp)
    formatted_result = format_value_dt(result, timestamp)
    log_file.write(formatted_result + "\n")
