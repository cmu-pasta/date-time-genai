
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timezone, timedelta
def calculate_time_since_epoch(timestamp: datetime) -> float:
    # Step 1: Define the Unix epoch (January 1, 1970, 00:00:00 UTC)
    # It's crucial to define the epoch as timezone-aware UTC.
    epoch_start = datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

    # Step 2: Ensure the input timestamp is also in UTC for a correct comparison.
    # If the timestamp is naive, it's often best to assume UTC for epoch calculations
    # or to explicitly define its intended timezone before conversion.
    # For robustness, we convert any timezone-aware datetime to UTC,
    # and if it's naive, we localize it to UTC.
    if timestamp.tzinfo is None:
        # If naive, assume it's UTC for this calculation, or localize it.
        # Localizing to UTC is a common and safe approach here.
        standardized_timestamp = timestamp.replace(tzinfo=timezone.utc)
    else:
        # If aware, convert to UTC
        standardized_timestamp = timestamp.astimezone(timezone.utc)

    # Step 3: Calculate the difference between the timestamp and the epoch
    time_difference: timedelta = standardized_timestamp - epoch_start

    # Step 4: Convert the timedelta to total seconds as a float
    # total_seconds() handles days, hours, minutes, seconds, and microseconds correctly.
    elapsed_seconds: float = time_difference.total_seconds()

    # Step 5: Return the result
    return elapsed_seconds

# Entry point: calculate_time_since_epoch(timestamp: datetime) -> float

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_30_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_time_since_epoch(timestamp):
    result = calculate_time_since_epoch(timestamp)
    formatted_result = format_value_dt(result, timestamp)
    log_file.write(formatted_result + "\n")
