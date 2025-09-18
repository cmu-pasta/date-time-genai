
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def calculate_hours_in_month(input_date: date) -> int:
    # Step 1: Extract year and month from the input date
    year = input_date.year
    month = input_date.month
    
    # Step 2: Calculate the number of days in the given month
    # Handle different months and leap years
    if month in [1, 3, 5, 7, 8, 10, 12]:  # Months with 31 days
        days_in_month = 31
    elif month in [4, 6, 9, 11]:  # Months with 30 days
        days_in_month = 30
    else:  # February (month == 2)
        # Check if it's a leap year
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            days_in_month = 29  # Leap year February
        else:
            days_in_month = 28  # Regular February
    
    # Step 3: Calculate total hours (days * 24 hours per day)
    total_hours = days_in_month * 24
    
    # Step 4: Return the result as an integer
    return total_hours

# Entry point: calculate_hours_in_month(input_date: date) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_42txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_calculate_hours_in_month(input_date):
    result = calculate_hours_in_month(input_date)
    formatted_result = format_value_dt(result, input_date)
    log_file.write(formatted_result + "\n")
