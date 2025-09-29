
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_n_business_days_after(start_date: datetime, n_business_days: int) -> datetime:
    # Initialize the current date to the start_date
    current_date = start_date
    
    # Iterate until N business days have been counted
    while n_business_days > 0:
        # Move to the next calendar day
        current_date += timedelta(days=1)
        
        # Check if the current day is a weekday (Monday=0 to Friday=4)
        # Saturday is 5, Sunday is 6
        if 0 <= current_date.weekday() <= 4:
            # If it's a business day, decrement the counter
            n_business_days -= 1
            
    return current_date

# Entry point: find_n_business_days_after(start_date: datetime, n_business_days: int) -> datetime

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_14_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), timestamp_strategy())
def test_find_n_business_days_after(start_date, n_business_days):
    result = find_n_business_days_after(start_date, n_business_days)
    formatted_result = format_value_dt(result, start_date, n_business_days)
    log_file.write(formatted_result + "\n")
