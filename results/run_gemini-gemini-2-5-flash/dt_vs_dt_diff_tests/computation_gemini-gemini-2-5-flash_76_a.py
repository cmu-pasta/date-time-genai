
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def convert_datetime_to_days_since_reference(target_dt: datetime, reference_dt: datetime) -> int:
    # Step 1: Calculate the difference between the target datetime and the reference datetime.
    # This results in a timedelta object.
    time_difference: timedelta = target_dt - reference_dt
    
    # Step 2: Extract the 'days' attribute from the timedelta object.
    # This gives the number of full days as an integer.
    number_of_days: int = time_difference.days
    
    # Step 3: Return the calculated number of days.
    return number_of_days

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_76_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_convert_datetime_to_days_since_reference(target_dt, reference_dt):
    result = convert_datetime_to_days_since_reference(target_dt, reference_dt)
    formatted_result = format_value_dt(result, target_dt, reference_dt)
    log_file.write(formatted_result + "\n")
