
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def midpoint_datetime(dt1: datetime, dt2: datetime) -> datetime:
    """
    Compute the exact midpoint datetime between two given datetimes.

    Args:
        dt1: A datetime instance.
        dt2: A datetime instance.

    Returns:
        A datetime representing the exact halfway point between dt1 and dt2.

    Raises:
        ValueError: If one datetime is timezone-aware and the other is naive.
    """
    # Step 1: Validate timezone awareness compatibility
    if (dt1.tzinfo is None) != (dt2.tzinfo is None):
        raise ValueError("Both datetimes must be either naive or timezone-aware.")

    # Step 2: Identify earlier and later datetimes
    earlier = dt1 if dt1 <= dt2 else dt2
    later = dt2 if dt1 <= dt2 else dt1

    # Step 3: Compute the midpoint
    delta: timedelta = later - earlier
    midpoint = earlier + (delta / 2)

    return midpoint

# Entry point: midpoint_datetime(dt1: datetime, dt2: datetime) -> datetime

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_32txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_midpoint_datetime(dt1, dt2):
    result = midpoint_datetime(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
