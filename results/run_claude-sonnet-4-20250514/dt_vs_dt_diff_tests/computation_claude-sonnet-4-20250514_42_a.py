
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_hours_in_month(dt: datetime) -> int:
    # Step 1: Extract year and month from the datetime object
    year = dt.year
    month = dt.month
    
    # Step 2: Calculate the first day of the next month
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    
    # Step 3: Calculate the first day of current month
    first_day_current_month = datetime(year, month, 1)
    
    # Step 4: Calculate the difference to get number of days in the month
    days_in_month = (next_month - first_day_current_month).days
    
    # Step 5: Convert days to hours (24 hours per day)
    hours_in_month = days_in_month * 24
    
    return hours_in_month

# Entry point: calculate_hours_in_month(dt: datetime) -> int

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_42_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_hours_in_month(dt):
    result = calculate_hours_in_month(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
