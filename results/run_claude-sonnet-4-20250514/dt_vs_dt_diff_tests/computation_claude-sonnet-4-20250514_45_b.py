
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def calculate_business_days_remaining(given_date: datetime) -> int:
    # Step 1: Find the last day of the current month
    # Get the first day of the next month
    if given_date.month == 12:
        first_day_next_month = datetime(given_date.year + 1, 1, 1)
    else:
        first_day_next_month = datetime(given_date.year, given_date.month + 1, 1)
    
    # Last day of current month is one day before the first day of next month
    last_day_current_month = first_day_next_month - timedelta(days=1)
    
    # Step 2: Count business days from the day after given_date to last day of month
    business_days_count = 0
    current_date = given_date + timedelta(days=1)  # Start from the next day
    
    # Step 3: Iterate through each day and count weekdays
    while current_date <= last_day_current_month:
        # Check if it's a weekday (Monday=0, Tuesday=1, ..., Friday=4, Saturday=5, Sunday=6)
        if current_date.weekday() < 5:  # 0-4 are weekdays
            business_days_count += 1
        current_date += timedelta(days=1)
    
    # Step 4: Return the count
    return business_days_count

# Entry point: calculate_business_days_remaining(given_date: datetime) -> int

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_45_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_business_days_remaining(given_date):
    result = calculate_business_days_remaining(given_date)
    formatted_result = format_value_dt(result, given_date)
    log_file.write(formatted_result + "\n")
