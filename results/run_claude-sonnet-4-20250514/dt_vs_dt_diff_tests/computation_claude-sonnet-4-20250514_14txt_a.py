
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_date_after_business_days(start_date: datetime, business_days: int) -> datetime:
    # Start from the given date
    current_date = start_date
    days_counted = 0
    
    # Keep adding days until we've counted the required number of business days
    while days_counted < business_days:
        # Move to the next day
        current_date += timedelta(days=1)
        
        # Check if it's a weekday (Monday=0 to Friday=4)
        if current_date.weekday() < 5:
            days_counted += 1
    
    return current_date

# Entry point: find_date_after_business_days(start_date: datetime, business_days: int) -> datetime

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_14txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), timestamp_strategy())
def test_find_date_after_business_days(start_date, business_days):
    result = find_date_after_business_days(start_date, business_days)
    formatted_result = format_value_dt(result, start_date, business_days)
    log_file.write(formatted_result + "\n")
