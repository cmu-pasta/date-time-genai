
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time
def calculate_decimal_time(t_of_day: time) -> float:
    # Step 1: Extract hours, minutes, and seconds from the time object
    hours = t_of_day.hour
    minutes = t_of_day.minute
    seconds = t_of_day.second
    
    # Step 2: Calculate the decimal time representation
    # This involves converting minutes and seconds into their fractional hour equivalents
    decimal_time = hours + (minutes / 60.0) + (seconds / 3600.0)
    
    # Step 3: Return the result as a float
    return decimal_time

# Entry point: calculate_decimal_time(t_of_day: time) -> float

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_99_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy())
def test_calculate_decimal_time(t_of_day):
    result = calculate_decimal_time(t_of_day)
    formatted_result = format_value_dt(result, t_of_day)
    log_file.write(formatted_result + "\n")
