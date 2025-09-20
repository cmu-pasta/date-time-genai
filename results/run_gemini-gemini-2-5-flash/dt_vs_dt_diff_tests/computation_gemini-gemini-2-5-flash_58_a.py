
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta, timezone
def convert_timestamp_to_new_epoch(
    source_timestamp_value: float, 
    source_epoch_datetime: datetime, 
    target_epoch_datetime: datetime
) -> float:
    """
    Converts a timestamp from its original epoch to a new target epoch.

    Args:
        source_timestamp_value: The numerical timestamp (e.g., seconds)
                                relative to the source epoch.
        source_epoch_datetime: A datetime object representing the start
                               of the source epoch (e.g., Unix epoch: Jan 1, 1970 UTC).
        target_epoch_datetime: A datetime object representing the start
                               of the target epoch (e.g., Windows epoch: Jan 1, 1601 UTC).

    Returns:
        The numerical timestamp relative to the target epoch.
    """
    # Step 1: Convert the source timestamp value to an absolute datetime object.
    # We assume source_timestamp_value is in seconds.
    absolute_datetime = source_epoch_datetime + timedelta(seconds=source_timestamp_value)

    # Step 2: Calculate the difference between the target epoch and the absolute datetime.
    # This timedelta represents the duration from the target epoch to the point in time.
    time_difference_from_target_epoch = absolute_datetime - target_epoch_datetime

    # Step 3: Convert the timedelta to the numerical timestamp in seconds.
    new_timestamp_value = time_difference_from_target_epoch.total_seconds()

    return new_timestamp_value

# Entry point: convert_timestamp_to_new_epoch(source_timestamp_value: float, source_epoch_datetime: datetime, target_epoch_datetime: datetime) -> float

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_58_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(float_strategy(), datetime_strategy(), datetime_strategy())
def test_convert_timestamp_to_new_epoch(source_timestamp_value, source_epoch_datetime, target_epoch_datetime):
    result = convert_timestamp_to_new_epoch(source_timestamp_value, source_epoch_datetime, target_epoch_datetime)
    formatted_result = format_value_dt(result, source_timestamp_value, source_epoch_datetime, target_epoch_datetime)
    log_file.write(formatted_result + "\n")
