
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time
def minutes_elapsed_today(current_time: time) -> int:
    # Step 1: Extract hours and minutes from the input time
    hours = current_time.hour
    minutes = current_time.minute
    
    # Step 2: Compute total elapsed minutes since midnight
    total_minutes = hours * 60 + minutes
    
    # Step 3: Return the total minutes as an integer
    return total_minutes

# Entry point: minutes_elapsed_today(current_time: time) -> int

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_49txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy())
def test_minutes_elapsed_today(current_time):
    result = minutes_elapsed_today(current_time)
    formatted_result = format_value_dt(result, current_time)
    log_file.write(formatted_result + "\n")
