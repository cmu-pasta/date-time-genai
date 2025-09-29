
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def calculate_weekends_between_dates(dt1: datetime, dt2: datetime) -> int:
    # Step 1: Ensure we have the correct date order and extract date parts
    start_date = min(dt1, dt2).date()
    end_date = max(dt1, dt2).date()
    
    # Step 2: Initialize weekend counter
    weekend_count = 0
    current_date = start_date
    
    # Step 3: Iterate through each date in the range (inclusive)
    while current_date <= end_date:
        # Step 4: Check if current date is a weekend day (Saturday=5, Sunday=6)
        if current_date.weekday() in [5, 6]:
            weekend_count += 1
        current_date += timedelta(days=1)
    
    # Step 5: Return the total count of weekend days
    return weekend_count

# Entry point: calculate_weekends_between_dates(dt1: datetime, dt2: datetime) -> int

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_15_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_weekends_between_dates(dt1, dt2):
    result = calculate_weekends_between_dates(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
