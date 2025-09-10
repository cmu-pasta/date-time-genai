
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def find_midpoint_datetime(dt1: datetime, dt2: datetime) -> datetime:
    # Step 1: Ensure dt1 is the earlier datetime
    if dt1 > dt2:
        dt1, dt2 = dt2, dt1
    
    # Step 2: Calculate the difference between the two datetimes
    delta = dt2 - dt1
    
    # Step 3: Calculate half of the time difference
    half_delta = delta / 2
    
    # Step 4: Add half of the delta to the earlier datetime to get midpoint
    midpoint = dt1 + half_delta
    
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

if not os.path.exists(".logs/diff_test_logs"):
    os.makedirs(".logs/diff_test_logs")
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_27txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_find_midpoint_datetime(dt1, dt2):
    result = find_midpoint_datetime(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
