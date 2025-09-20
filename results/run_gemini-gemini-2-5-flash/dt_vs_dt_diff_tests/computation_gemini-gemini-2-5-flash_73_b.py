
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, time
def is_within_business_hours(dt: datetime) -> bool:
    # Step 1: Define the start and end of business hours
    # Business hours are 9 AM to 5 PM
    business_start = time(9, 0, 0) # 9:00:00 AM
    business_end = time(17, 0, 0)  # 5:00:00 PM (17:00:00 in 24-hour format)
    
    # Step 2: Extract the time component from the input datetime object
    current_time = dt.time()
    
    # Step 3: Compare the current_time with the business hours
    # The time is within business hours if it's >= business_start and < business_end
    # This means 9:00:00 AM is included, but 5:00:00 PM is not.
    is_business_hour = business_start <= current_time < business_end
    
    # Step 4: Return the boolean result
    return is_business_hour

# Entry point: is_within_business_hours(dt: datetime) -> bool

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_73_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_is_within_business_hours(dt):
    result = is_within_business_hours(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
