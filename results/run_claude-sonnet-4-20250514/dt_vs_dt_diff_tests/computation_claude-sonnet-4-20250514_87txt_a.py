
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_nanoseconds_difference(dt1: datetime, dt2: datetime) -> int:
    # Step 1: Calculate the difference between timestamps
    difference = abs(dt2 - dt1)  # Using abs to ensure a positive difference
    
    # Step 2: Convert timedelta components to nanoseconds
    # timedelta has: days, seconds, microseconds
    days_ns = difference.days * 24 * 60 * 60 * 1_000_000_000  # days to nanoseconds
    seconds_ns = difference.seconds * 1_000_000_000  # seconds to nanoseconds
    microseconds_ns = difference.microseconds * 1_000  # microseconds to nanoseconds
    
    # Step 3: Sum all components to get total nanoseconds
    total_nanoseconds = days_ns + seconds_ns + microseconds_ns
    
    # Step 4: Return the result as an integer
    return total_nanoseconds

# Entry point: calculate_nanoseconds_difference(dt1: datetime, dt2: datetime) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_87txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_nanoseconds_difference(dt1, dt2):
    result = calculate_nanoseconds_difference(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
