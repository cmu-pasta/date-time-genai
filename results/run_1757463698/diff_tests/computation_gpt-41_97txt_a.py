
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def get_start_of_next_hour(dt: datetime) -> datetime:
    # Step 1: Replace minutes, seconds, and microseconds to zero for the start of current hour
    current_hour_start = dt.replace(minute=0, second=0, microsecond=0)
    
    # Step 2: Add one hour to get the start time of the next hour
    next_hour_start = current_hour_start + timedelta(hours=1)
    
    # Step 3: Return the result as a datetime object
    return next_hour_start

# Entry point: get_start_of_next_hour(dt: datetime) -> datetime

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_97txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_get_start_of_next_hour(dt):
    result = get_start_of_next_hour(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
