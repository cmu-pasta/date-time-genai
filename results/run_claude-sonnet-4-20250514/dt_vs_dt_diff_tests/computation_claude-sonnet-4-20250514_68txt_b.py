
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_labor_day(year: int) -> datetime:
    # Step 1: Create September 1st of the given year
    sep_first = datetime(year, 9, 1)
    
    # Step 2: Find the weekday (Monday = 0, Sunday = 6)
    weekday = sep_first.weekday()
    
    # Step 3: Calculate days to add to reach the first Monday
    if weekday == 0:  # September 1st is already Monday
        days_to_add = 0
    else:  # Add days to reach the next Monday
        days_to_add = 7 - weekday
    
    # Step 4: Calculate Labor Day by adding the required days
    labor_day = sep_first + timedelta(days=days_to_add)
    
    # Step 5: Return the result as a datetime object
    return labor_day

# Entry point: find_labor_day(year: int) -> datetime

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_68txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_labor_day(year):
    result = find_labor_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
