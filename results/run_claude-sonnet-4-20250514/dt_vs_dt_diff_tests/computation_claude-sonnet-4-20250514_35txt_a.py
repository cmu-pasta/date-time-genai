
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_last_business_day_of_month(input_date: date) -> date:
    # Step 1: Find the last day of the month
    if input_date.month == 12:
        # If December, next month is January of next year
        first_day_next_month = date(input_date.year + 1, 1, 1)
    else:
        # Otherwise, just increment the month
        first_day_next_month = date(input_date.year, input_date.month + 1, 1)
    
    # Last day of current month is one day before first day of next month
    last_day_of_month = first_day_next_month - timedelta(days=1)
    
    # Step 2: Find the last business day by going backwards from the last day
    current_day = last_day_of_month
    while current_day.weekday() >= 5:  # Saturday=5, Sunday=6 are weekends
        current_day = current_day - timedelta(days=1)
    
    return current_day

# Entry point: find_last_business_day_of_month(input_date: date) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_35txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_find_last_business_day_of_month(input_date):
    result = find_last_business_day_of_month(input_date)
    formatted_result = format_value_dt(result, input_date)
    log_file.write(formatted_result + "\n")
