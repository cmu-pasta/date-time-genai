
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date, time
def calculate_minutes_difference_times(t1: time, t2: time) -> int:
    # Step 1: Combine each time with an arbitrary common date to create datetime objects.
    # Using date.min ensures we have a valid date part for subtraction,
    # without affecting the time difference.
    dt1 = datetime.combine(date.min, t1)
    dt2 = datetime.combine(date.min, t2)
    
    # Step 2: Calculate the difference between the two datetime objects.
    # This results in a timedelta object.
    time_difference = dt2 - dt1
    
    # Step 3: Get the total number of seconds from the timedelta and convert to minutes.
    # Use abs() to ensure the difference is always positive, regardless of input order.
    total_minutes = abs(int(time_difference.total_seconds() / 60))
    
    # Step 4: Return the result as an integer.
    return total_minutes

# Entry point: calculate_minutes_difference_times(t1: time, t2: time) -> int

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_33_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy(), time_strategy())
def test_calculate_minutes_difference_times(t1, t2):
    result = calculate_minutes_difference_times(t1, t2)
    formatted_result = format_value_dt(result, t1, t2)
    log_file.write(formatted_result + "\n")
