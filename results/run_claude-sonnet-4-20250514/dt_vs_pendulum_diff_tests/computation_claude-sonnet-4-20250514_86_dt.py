
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_presidents_day(year: int) -> date:
    # Step 1: Find February 1st of the given year
    feb_first = date(year, 2, 1)
    
    # Step 2: Calculate days to add to reach the first Monday
    # weekday() returns 0 for Monday, 1 for Tuesday, etc.
    # If Feb 1st is Monday, add 0 days; otherwise calculate days to next Monday
    days_to_first_monday = (-feb_first.weekday()) % 7
    
    # Step 3: Find the first Monday of February
    first_monday = feb_first + timedelta(days=days_to_first_monday)
    
    # Step 4: Find the third Monday (Presidents' Day) by adding 14 days
    presidents_day = first_monday + timedelta(days=14)
    
    # Step 5: Return the result
    return presidents_day

# Entry point: find_presidents_day(year: int) -> date

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_86_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_presidents_day(year):
    result = find_presidents_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
