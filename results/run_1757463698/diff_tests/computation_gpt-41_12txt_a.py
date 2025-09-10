
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def subtract_timestamps_return_hours_minutes(dt1: datetime, dt2: datetime) -> int:
    # Step 1: Subtract one timestamp from the other to get a timedelta
    duration = abs(dt2 - dt1)
    
    # Step 2: Calculate the total number of hours and minutes
    total_seconds = duration.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    
    # Step 3: Combine the result into a single integer representation
    # For distinctness, we can return hours*100 + minutes as integer (e.g., 225 means 2 hr 25 min)
    return hours * 100 + minutes

# Entry point: subtract_timestamps_return_hours_minutes(dt1: datetime, dt2: datetime) -> int

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_12txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_subtract_timestamps_return_hours_minutes(dt1, dt2):
    result = subtract_timestamps_return_hours_minutes(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
