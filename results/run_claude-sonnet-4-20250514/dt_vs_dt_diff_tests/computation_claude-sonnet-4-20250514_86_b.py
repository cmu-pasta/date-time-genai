
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def find_presidents_day(year: int) -> datetime:
    # Step 1: Create February 1st of the given year
    feb_first = datetime(year, 2, 1)
    
    # Step 2: Find what day of the week February 1st is (Monday = 0, Sunday = 6)
    weekday = feb_first.weekday()
    
    # Step 3: Calculate days to add to get to the first Monday
    days_to_first_monday = (7 - weekday) % 7
    
    # Step 4: Calculate the first Monday of February
    first_monday = datetime(year, 2, 1 + days_to_first_monday)
    
    # Step 5: Add 14 days to get the third Monday (Presidents' Day)
    presidents_day = datetime(first_monday.year, first_monday.month, first_monday.day + 14)
    
    return presidents_day

# Entry point: find_presidents_day(year: int) -> datetime

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_86_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_presidents_day(year):
    result = find_presidents_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
