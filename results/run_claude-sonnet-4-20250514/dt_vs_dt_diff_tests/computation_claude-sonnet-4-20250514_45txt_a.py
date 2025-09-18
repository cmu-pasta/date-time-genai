
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
import calendar
def calculate_business_days_remaining(given_date: date) -> int:
    # Find the last day of the current month
    last_day = calendar.monthrange(given_date.year, given_date.month)[1]
    end_of_month = date(given_date.year, given_date.month, last_day)
    
    business_days = 0
    current_date = given_date
    
    # Count business days from given_date to end of month (inclusive)
    while current_date <= end_of_month:
        # Monday is 0, Sunday is 6. Business days are 0-4 (Monday-Friday)
        if current_date.weekday() < 5:
            business_days += 1
        current_date += timedelta(days=1)
    
    return business_days

# Entry point: calculate_business_days_remaining(given_date: date) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_45txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_calculate_business_days_remaining(given_date):
    result = calculate_business_days_remaining(given_date)
    formatted_result = format_value_dt(result, given_date)
    log_file.write(formatted_result + "\n")
