
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_columbus_day(year: int) -> datetime:
    # Step 1: Create October 1st of the given year
    october_first = datetime(year, 10, 1)
    
    # Step 2: Calculate days until the first Monday
    # weekday() returns 0 for Monday, 1 for Tuesday, etc.
    days_until_first_monday = (7 - october_first.weekday()) % 7
    
    # Step 3: Calculate the first Monday
    first_monday = october_first + timedelta(days=days_until_first_monday)
    
    # Step 4: Calculate the second Monday (Columbus Day)
    columbus_day = first_monday + timedelta(days=7)
    
    return columbus_day

# Entry point: find_columbus_day(year: int) -> datetime

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_77_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_columbus_day(year):
    result = find_columbus_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
