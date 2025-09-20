
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_date_n_business_days_after(start_date: datetime, n_business_days: int) -> datetime:
    current_date = start_date
    days_added_to_count = 0

    # If n_business_days is 0, return the start_date directly.
    # Otherwise, loop to find the future date.
    if n_business_days == 0:
        return start_date

    # Loop until the required number of business days have been counted.
    # The loop will always increment the day *before* checking if it's a business day,
    # ensuring we find a date *after* the start_date.
    while days_added_to_count < n_business_days:
        current_date += timedelta(days=1) # Move to the next day

        # Check if the current_date is a weekday (Monday=0 to Friday=4)
        if 0 <= current_date.weekday() <= 4:
            days_added_to_count += 1
            
    return current_date

# Entry point: find_date_n_business_days_after(start_date: datetime, n_business_days: int) -> datetime

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_14_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), timestamp_strategy())
def test_find_date_n_business_days_after(start_date, n_business_days):
    result = find_date_n_business_days_after(start_date, n_business_days)
    formatted_result = format_value_dt(result, start_date, n_business_days)
    log_file.write(formatted_result + "\n")
