
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_nanoseconds_difference(dt1: datetime, dt2: datetime) -> int:
    # Step 1: Calculate the difference between the two timestamps
    time_diff = dt2 - dt1
    
    # Step 2: Extract components from timedelta
    days = time_diff.days
    seconds = time_diff.seconds
    microseconds = time_diff.microseconds
    
    # Step 3: Convert everything to nanoseconds
    # 1 day = 86400 seconds = 86400 * 1,000,000,000 nanoseconds
    # 1 second = 1,000,000,000 nanoseconds  
    # 1 microsecond = 1,000 nanoseconds
    total_nanoseconds = (days * 86400 * 1000000000) + (seconds * 1000000000) + (microseconds * 1000)
    
    # Step 4: Return the absolute value to ensure positive result
    return abs(total_nanoseconds)

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_87_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_nanoseconds_difference(dt1, dt2):
    result = calculate_nanoseconds_difference(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
