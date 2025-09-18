
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_mlk_day(year: int) -> datetime:
    # Step 1: Get January 1st of the given year
    jan_first = datetime(year, 1, 1)
    
    # Step 2: Find the first Monday of January
    # weekday() returns 0 for Monday, 1 for Tuesday, ..., 6 for Sunday
    days_until_monday = (7 - jan_first.weekday()) % 7
    first_monday = jan_first + timedelta(days=days_until_monday)
    
    # Step 3: Add 14 days (2 weeks) to get the third Monday
    third_monday = first_monday + timedelta(days=14)
    
    return third_monday

# Entry point: find_mlk_day(year: int) -> datetime

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_92txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_mlk_day(year):
    result = find_mlk_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
