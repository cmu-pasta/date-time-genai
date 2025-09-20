
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def calculate_business_days_remaining(dt_current: datetime) -> int:
    # Step 1: Determine the last day of the current month
    # To get the first day of the next month:
    # If it's December, the next month is January of the next year.
    if dt_current.month == 12:
        next_month_year = dt_current.year + 1
        next_month = 1
    else:
        next_month_year = dt_current.year
        next_month = dt_current.month + 1
    
    # Create a datetime object for the first day of the next month
    first_day_of_next_month = datetime(next_month_year, next_month, 1)
    
    # Subtract one day to get the last day of the current month
    last_day_of_month = first_day_of_next_month - timedelta(days=1)
    
    # Step 2: Initialize a counter for business days
    business_days_count = 0
    
    # Step 3: Iterate from the current date up to and including the last day of the month
    current_day_iterator = dt_current
    while current_day_iterator <= last_day_of_month:
        # Step 4: Check if the current day is a business day (Monday to Friday)
        # weekday() returns 0 for Monday, 1 for Tuesday, ..., 4 for Friday, 5 for Saturday, 6 for Sunday.
        if current_day_iterator.weekday() < 5:  # Monday (0) to Friday (4)
            business_days_count += 1
        
        # Move to the next day
        current_day_iterator += timedelta(days=1)
        # Ensure we only compare dates, not times when incrementing across midnight
        # Or, just ensure the iterator is a date-only object if only dates matter.
        # For simplicity and sticking to datetime, we just add timedelta.
        # The time component won't affect weekday() or date comparisons here.
            
    # Step 5: Return the total count
    return business_days_count

# Entry point: calculate_business_days_remaining(dt_current: datetime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_45_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_business_days_remaining(dt_current):
    result = calculate_business_days_remaining(dt_current)
    formatted_result = format_value_dt(result, dt_current)
    log_file.write(formatted_result + "\n")
