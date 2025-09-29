
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_mlk_day(year: int) -> date:
    # Step 1: Get January 1st of the given year
    jan_first = date(year, 1, 1)
    
    # Step 2: Find what day of the week January 1st is (0=Monday, 6=Sunday)
    jan_first_weekday = jan_first.weekday()
    
    # Step 3: Calculate days to add to get to the first Monday
    # If Jan 1st is Monday (0), we need 0 days
    # If Jan 1st is Tuesday (1), we need 6 days
    # If Jan 1st is Wednesday (2), we need 5 days, etc.
    days_to_first_monday = (7 - jan_first_weekday) % 7
    
    # Step 4: Find the first Monday of January
    first_monday = jan_first + timedelta(days=days_to_first_monday)
    
    # Step 5: Add 14 days (2 weeks) to get the third Monday
    third_monday = first_monday + timedelta(days=14)
    
    return third_monday

# Entry point: find_mlk_day(year: int) -> date

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_92_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_mlk_day(year):
    result = find_mlk_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
