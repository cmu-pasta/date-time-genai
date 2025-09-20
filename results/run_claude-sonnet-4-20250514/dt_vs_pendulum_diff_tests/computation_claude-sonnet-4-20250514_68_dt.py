
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_labor_day(year: int) -> datetime:
    # Step 1: Create September 1st of the given year
    sep_first = datetime(year, 9, 1)
    
    # Step 2: Find what day of the week September 1st falls on
    # weekday() returns 0 for Monday, 1 for Tuesday, ..., 6 for Sunday
    weekday = sep_first.weekday()
    
    # Step 3: Calculate how many days to add to get to the first Monday
    # If it's already Monday (0), add 0 days
    # Otherwise, add enough days to reach the next Monday
    days_to_add = (7 - weekday) % 7
    
    # Step 4: Calculate Labor Day by adding the required days
    labor_day = sep_first + timedelta(days=days_to_add)
    
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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_68_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_labor_day(year):
    result = find_labor_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
