
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def find_midpoint_datetime(dt1: datetime, dt2: datetime) -> datetime:
    # Step 1: Determine which datetime is earlier and which is later
    earlier_dt = min(dt1, dt2)
    later_dt = max(dt1, dt2)
    
    # Step 2: Calculate the time difference between the two datetimes
    time_difference = later_dt - earlier_dt
    
    # Step 3: Find half of the time difference
    half_difference = time_difference / 2
    
    # Step 4: Add half the difference to the earlier datetime to get the midpoint
    midpoint = earlier_dt + half_difference
    
    # Step 5: Return the midpoint datetime
    return midpoint

# Entry point: find_midpoint_datetime(dt1: datetime, dt2: datetime) -> datetime

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_26txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_find_midpoint_datetime(dt1, dt2):
    result = find_midpoint_datetime(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
