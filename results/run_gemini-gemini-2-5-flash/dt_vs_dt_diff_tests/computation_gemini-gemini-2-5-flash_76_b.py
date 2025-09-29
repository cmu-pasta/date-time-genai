
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def convert_datetime_to_days_since_reference(target_dt: datetime, reference_dt: datetime) -> int:
    # Step 1: Calculate the difference between the target_dt and the reference_dt
    # This will result in a timedelta object.
    time_difference = target_dt - reference_dt
    
    # Step 2: Extract the number of days from the timedelta object.
    # The .days attribute gives the difference in full days as an integer.
    days_since_reference = time_difference.days
    
    # Step 3: Return the integer representing the number of days.
    return days_since_reference

# Entry point: convert_datetime_to_days_since_reference(target_dt: datetime, reference_dt: datetime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_76_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_convert_datetime_to_days_since_reference(target_dt, reference_dt):
    result = convert_datetime_to_days_since_reference(target_dt, reference_dt)
    formatted_result = format_value_dt(result, target_dt, reference_dt)
    log_file.write(formatted_result + "\n")
