
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date
def find_first_day_of_spring(year: int) -> date:
    # Step 1: The spring equinox typically falls on March 20 or March 21
    # For most years in recent centuries, March 20 is the standard date
    # We'll use March 20 as the default first day of spring
    
    # Step 2: Create the date for March 20 of the given year
    spring_date = date(year, 3, 20)
    
    # Step 3: Return the date
    return spring_date

# Entry point: find_first_day_of_spring(year: int) -> date

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_44_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_first_day_of_spring(year):
    result = find_first_day_of_spring(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
