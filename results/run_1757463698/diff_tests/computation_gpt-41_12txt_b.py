
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def duration_in_hours_and_minutes(ts1: datetime, ts2: datetime) -> int:
    """
    Subtract two timestamps (datetime objects) and return the duration in hours and minutes.
    Returns the total duration as the number of hours * 100 + minutes (e.g. 3 hours 45 minutes -> 345).
    """
    # Step 1: Calculate absolute difference
    delta = abs(ts2 - ts1)
    # Step 2: Extract total seconds
    total_seconds = int(delta.total_seconds())
    # Step 3: Compute hours and minutes
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    # Step 4: Combine hours and minutes in a simple integer format
    result = hours * 100 + minutes
    return result

# Entry point: duration_in_hours_and_minutes(ts1: datetime, ts2: datetime) -> int

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_12txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_duration_in_hours_and_minutes(ts1, ts2):
    result = duration_in_hours_and_minutes(ts1, ts2)
    formatted_result = format_value_dt(result, ts1, ts2)
    log_file.write(formatted_result + "\n")
