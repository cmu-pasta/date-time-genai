
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def find_labor_day(year: int) -> date:
    # Start with September 1st of the given year
    sept_first = date(year, 9, 1)
    
    # Get the weekday (0=Monday, 1=Tuesday, ..., 6=Sunday)
    weekday = sept_first.weekday()
    
    # Calculate days to add to get to the first Monday
    if weekday == 0:
        days_to_add = 0  # Already Monday
    else:
        days_to_add = 7 - weekday
    
    # Calculate Labor Day by adding the necessary days
    labor_day = date(year, 9, 1 + days_to_add)
    return labor_day

# Entry point: find_labor_day(year: int) -> date

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_68_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_labor_day(year):
    result = find_labor_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
