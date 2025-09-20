
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_last_business_day_of_month(dt: datetime) -> datetime:
    # Step 1: Find the last day of the month
    # Get the first day of the next month
    if dt.month == 12:
        next_month_first = datetime(dt.year + 1, 1, 1)
    else:
        next_month_first = datetime(dt.year, dt.month + 1, 1)
    
    # Get the last day of the current month
    last_day_of_month = next_month_first - timedelta(days=1)
    
    # Step 2: Find the last business day
    # Start from the last day and go backwards until we find a weekday
    current_day = last_day_of_month
    
    # weekday() returns 0 for Monday, 6 for Sunday
    # Business days are Monday (0) through Friday (4)
    while current_day.weekday() > 4:  # Saturday is 5, Sunday is 6
        current_day = current_day - timedelta(days=1)
    
    return current_day

# Entry point: find_last_business_day_of_month(dt: datetime) -> datetime

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_35_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_last_business_day_of_month(dt):
    result = find_last_business_day_of_month(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
