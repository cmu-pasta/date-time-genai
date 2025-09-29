
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time
def is_within_business_hours(input_time: time) -> bool:
    # Step 1: Define the start of business hours (9 AM)
    business_start = time(9, 0, 0)
    
    # Step 2: Define the end of business hours (5 PM)
    business_end = time(17, 0, 0) # 5 PM in 24-hour format

    # Step 3: Check if the input_time falls within the business hours range
    # It must be greater than or equal to business_start and strictly less than business_end
    is_within = (input_time >= business_start) and (input_time < business_end)
    
    # Step 4: Return the boolean result
    return is_within

# Entry point: is_within_business_hours(input_time: time) -> bool

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_73_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy())
def test_is_within_business_hours(input_time):
    result = is_within_business_hours(input_time)
    formatted_result = format_value_dt(result, input_time)
    log_file.write(formatted_result + "\n")
