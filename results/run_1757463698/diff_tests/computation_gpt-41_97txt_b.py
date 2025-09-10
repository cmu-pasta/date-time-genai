
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def get_start_of_next_hour(dt: datetime) -> datetime:
    # Step 1: Reset minutes, seconds, and microseconds to zero (start of the hour)
    start_of_current_hour = dt.replace(minute=0, second=0, microsecond=0)
    
    # Step 2: Add one hour to get the start of the next hour
    start_of_next_hour = start_of_current_hour + timedelta(hours=1)
    
    # Step 3: Return the computed datetime
    return start_of_next_hour

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_97txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_get_start_of_next_hour(dt):
    result = get_start_of_next_hour(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
