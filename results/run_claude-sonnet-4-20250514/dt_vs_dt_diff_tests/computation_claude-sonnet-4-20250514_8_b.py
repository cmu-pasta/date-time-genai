
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_last_day_of_month(dt: datetime) -> datetime:
    # Step 1: Extract year and month from input datetime
    year = dt.year
    month = dt.month
    
    # Step 2: Calculate next month and handle year rollover
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
    
    # Step 3: Create datetime for first day of next month
    first_day_next_month = datetime(next_year, next_month, 1, dt.hour, dt.minute, dt.second, dt.microsecond)
    
    # Step 4: Subtract one day to get last day of current month
    last_day_of_month = first_day_next_month - timedelta(days=1)
    
    # Step 5: Return the result
    return last_day_of_month

# Entry point: find_last_day_of_month(dt: datetime) -> datetime

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_8_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_last_day_of_month(dt):
    result = find_last_day_of_month(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
