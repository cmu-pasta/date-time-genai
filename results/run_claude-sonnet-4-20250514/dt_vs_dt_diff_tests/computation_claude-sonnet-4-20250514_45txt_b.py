
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
import calendar
def calculate_business_days_remaining(given_date: datetime) -> int:
    # Step 1: Find the last day of the current month
    year = given_date.year
    month = given_date.month
    last_day_of_month = calendar.monthrange(year, month)[1]
    end_of_month = datetime(year, month, last_day_of_month)
    
    # Step 2: Count business days from given_date to end of month (inclusive)
    business_days_count = 0
    current_date = given_date.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Step 3: Iterate through each day and count business days
    while current_date <= end_of_month:
        # Check if current day is a business day (Monday=0 to Friday=4)
        if current_date.weekday() < 5:  # 0-4 are business days
            business_days_count += 1
        current_date += timedelta(days=1)
    
    # Step 4: Return the count of business days
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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_45txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_business_days_remaining(given_date):
    result = calculate_business_days_remaining(given_date)
    formatted_result = format_value_dt(result, given_date)
    log_file.write(formatted_result + "\n")
