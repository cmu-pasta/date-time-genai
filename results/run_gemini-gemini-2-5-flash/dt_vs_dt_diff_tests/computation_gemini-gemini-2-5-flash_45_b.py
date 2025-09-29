
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def calculate_business_days_remaining_in_month(given_date: datetime) -> int:
    # Step 1: Initialize a counter for business days
    business_days_count = 0

    # Step 2: Determine the first day of the next month
    # This handles year rollovers correctly (e.g., December to January)
    if given_date.month == 12:
        first_day_next_month = datetime(given_date.year + 1, 1, 1)
    else:
        first_day_next_month = datetime(given_date.year, given_date.month + 1, 1)

    # Step 3: Determine the last day of the current month
    last_day_of_month = first_day_next_month - timedelta(days=1)

    # Step 4: Iterate from the given date to the last day of the month
    current_day = given_date.date() # Start from the date part of given_date
    while current_day <= last_day_of_month.date():
        # Step 5: Check if the current day is a weekday (Monday=0 to Friday=4)
        if 0 <= current_day.weekday() <= 4:
            business_days_count += 1
        
        # Move to the next day
        current_day += timedelta(days=1)

    # Step 6: Return the total count of business days
    return business_days_count

# Entry point: calculate_business_days_remaining_in_month(given_date: datetime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_45_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_business_days_remaining_in_month(given_date):
    result = calculate_business_days_remaining_in_month(given_date)
    formatted_result = format_value_dt(result, given_date)
    log_file.write(formatted_result + "\n")
