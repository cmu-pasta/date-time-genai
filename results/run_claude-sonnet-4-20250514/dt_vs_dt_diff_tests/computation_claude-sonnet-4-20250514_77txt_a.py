
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date, timedelta
def find_columbus_day(year: int) -> date:
    # Step 1: Create October 1st of the given year
    october_first = date(year, 10, 1)
    
    # Step 2: Find what day of the week October 1st is (0=Monday, 6=Sunday)
    weekday = october_first.weekday()
    
    # Step 3: Calculate days to add to reach the first Monday
    # If it's already Monday (0), we need 0 days
    # If it's Tuesday (1), we need 6 days, etc.
    days_to_first_monday = (7 - weekday) % 7
    
    # Step 4: Calculate the first Monday of October
    first_monday = october_first + timedelta(days=days_to_first_monday)
    
    # Step 5: Calculate the second Monday (Columbus Day)
    columbus_day = first_monday + timedelta(days=7)
    
    return columbus_day

# Entry point: find_columbus_day(year: int) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_77txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_columbus_day(year):
    result = find_columbus_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
