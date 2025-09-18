
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_total_minutes(start_time: datetime, end_time: datetime) -> float:
    # Step 1: Calculate the difference between the two datetime objects
    time_difference = end_time - start_time
    
    # Step 2: Get total seconds from the timedelta object
    total_seconds = time_difference.total_seconds()
    
    # Step 3: Convert seconds to minutes
    total_minutes = total_seconds / 60
    
    # Step 4: Return the absolute value to ensure positive result
    return abs(total_minutes)

# Entry point: calculate_total_minutes(start_time: datetime, end_time: datetime) -> float

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_51txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_total_minutes(start_time, end_time):
    result = calculate_total_minutes(start_time, end_time)
    formatted_result = format_value_dt(result, start_time, end_time)
    log_file.write(formatted_result + "\n")
