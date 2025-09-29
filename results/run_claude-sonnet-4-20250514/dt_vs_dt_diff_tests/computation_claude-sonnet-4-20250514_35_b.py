
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_last_business_day(dt: datetime) -> datetime:
    # Step 1: Find the last day of the month
    # Go to the first day of the next month, then subtract 1 day
    if dt.month == 12:
        next_month = dt.replace(year=dt.year + 1, month=1, day=1)
    else:
        next_month = dt.replace(month=dt.month + 1, day=1)
    
    last_day_of_month = next_month - timedelta(days=1)
    
    # Step 2: Work backwards from the last day until we find a business day
    current_date = last_day_of_month
    while current_date.weekday() > 4:  # 0-4 are Mon-Fri (business days), 5-6 are Sat-Sun
        current_date = current_date - timedelta(days=1)
    
    # Step 3: Return the last business day
    return current_date

# Entry point: find_last_business_day(dt: datetime) -> datetime

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_35_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_last_business_day(dt):
    result = find_last_business_day(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
