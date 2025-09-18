
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date
def find_presidents_day(year: int) -> date:
    # Step 1: Create February 1st of the given year
    feb_first = date(year, 2, 1)
    
    # Step 2: Find what day of the week February 1st falls on
    # weekday() returns 0 for Monday, 1 for Tuesday, ..., 6 for Sunday
    feb_first_weekday = feb_first.weekday()
    
    # Step 3: Calculate days to add to reach the first Monday of February
    # If Feb 1st is already Monday (0), we don't need to add any days
    # If Feb 1st is Tuesday (1), we need to add 6 days to reach next Monday
    days_to_first_monday = (7 - feb_first_weekday) % 7
    
    # Step 4: Calculate the first Monday of February
    first_monday = date(year, 2, 1 + days_to_first_monday)
    
    # Step 5: Add 14 days (2 weeks) to get the third Monday
    third_monday = date(year, 2, 1 + days_to_first_monday + 14)
    
    return third_monday

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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_86txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_presidents_day(year):
    result = find_presidents_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
