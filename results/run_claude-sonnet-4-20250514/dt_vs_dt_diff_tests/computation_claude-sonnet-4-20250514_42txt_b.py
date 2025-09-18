
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_hours_in_month(year: int, month: int) -> int:
    # Step 1: Create a datetime object for the first day of the given month
    first_day_current_month = datetime(year, month, 1)
    
    # Step 2: Calculate the first day of the next month
    if month == 12:
        # If December, next month is January of next year
        first_day_next_month = datetime(year + 1, 1, 1)
    else:
        # Otherwise, just increment the month
        first_day_next_month = datetime(year, month + 1, 1)
    
    # Step 3: Calculate the difference to get number of days in the month
    days_in_month = (first_day_next_month - first_day_current_month).days
    
    # Step 4: Calculate total hours (days * 24)
    hours_in_month = days_in_month * 24
    
    # Step 5: Return the result as integer
    return hours_in_month

# Entry point: calculate_hours_in_month(year: int, month: int) -> int

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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_42txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy())
def test_calculate_hours_in_month(year, month):
    result = calculate_hours_in_month(year, month)
    formatted_result = format_value_dt(result, year, month)
    log_file.write(formatted_result + "\n")
