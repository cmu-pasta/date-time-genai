
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_indigenous_peoples_day(year: int) -> datetime:
    # Step 1: Create October 1st for the given year
    october_first = datetime(year, 10, 1)
    
    # Step 2: Find what day of the week October 1st falls on
    weekday = october_first.weekday()  # 0=Monday, 1=Tuesday, ..., 6=Sunday
    
    # Step 3: Calculate days to add to reach the first Monday
    days_to_first_monday = (7 - weekday) % 7
    
    # Step 4: Find the first Monday of October
    first_monday = october_first + timedelta(days=days_to_first_monday)
    
    # Step 5: Find the second Monday (Indigenous Peoples' Day)
    second_monday = first_monday + timedelta(days=7)
    
    return second_monday

# Entry point: find_indigenous_peoples_day(year: int) -> datetime

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_98_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_indigenous_peoples_day(year):
    result = find_indigenous_peoples_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
