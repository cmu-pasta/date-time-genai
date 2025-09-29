
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_previous_friday(dt: datetime) -> datetime:
    # Step 1: Get the current weekday (Monday is 0, Friday is 4, Sunday is 6)
    current_weekday = dt.weekday()
    
    # Step 2: Define Friday's weekday index
    FRIDAY = 4
    
    # Step 3: Calculate the number of days to subtract to get to the previous Friday.
    # The expression (current_weekday - FRIDAY + 7) % 7 calculates how many days
    # have passed since the *last* Friday (inclusive of today if today is Friday).
    # For example:
    # If dt is Friday (4): (4 - 4 + 7) % 7 = 0. This means 0 days ago was Friday.
    # If dt is Saturday (5): (5 - 4 + 7) % 7 = 1. This means 1 day ago was Friday.
    # If dt is Monday (0): (0 - 4 + 7) % 7 = 3. This means 3 days ago was Friday.
    
    days_since_last_friday = (current_weekday - FRIDAY + 7) % 7
    
    # If the current date is a Friday (days_since_last_friday == 0),
    # we need to go back a full week to get the *previous* Friday.
    # Otherwise, we go back the calculated number of days.
    if days_since_last_friday == 0:
        days_to_subtract = 7
    else:
        days_to_subtract = days_since_last_friday
        
    # Step 4: Subtract the timedelta from the given date
    previous_friday = dt - timedelta(days=days_to_subtract)
    
    # Step 5: Return the resulting datetime object
    return previous_friday

# Entry point: find_previous_friday(dt: datetime) -> datetime

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_20_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_previous_friday(dt):
    result = find_previous_friday(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
