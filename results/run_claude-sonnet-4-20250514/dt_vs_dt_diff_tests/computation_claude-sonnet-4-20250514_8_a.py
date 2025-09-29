
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_last_day_of_month(dt: datetime) -> datetime:
    # Step 1: Extract year and month from the input date
    year = dt.year
    month = dt.month
    
    # Step 2: Calculate the first day of the next month
    if month == 12:
        # If current month is December, next month is January of next year
        next_month_first_day = datetime(year + 1, 1, 1)
    else:
        # Otherwise, just increment the month
        next_month_first_day = datetime(year, month + 1, 1)
    
    # Step 3: Get the last day of current month by subtracting one day
    last_day_of_month = next_month_first_day - timedelta(days=1)
    
    # Step 4: Return the result
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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_8_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_last_day_of_month(dt):
    result = find_last_day_of_month(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
