
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def find_indigenous_peoples_day(year: int) -> datetime:
    # Step 1: Get October 1st for the given year
    oct_first = datetime(year, 10, 1)
    
    # Step 2: Find what day of the week October 1st falls on
    weekday_oct_first = oct_first.weekday()  # Monday=0, Sunday=6
    
    # Step 3: Calculate days to add to get to the first Monday
    # If Oct 1st is Monday (0), add 0 days
    # If Oct 1st is Tuesday (1), add 6 days to get to next Monday
    # If Oct 1st is Wednesday (2), add 5 days, etc.
    days_to_first_monday = (7 - weekday_oct_first) % 7
    
    # Step 4: Calculate the first Monday of October
    first_monday = datetime(year, 10, 1 + days_to_first_monday)
    
    # Step 5: Add 7 days to get the second Monday
    second_monday = datetime(year, 10, 1 + days_to_first_monday + 7)
    
    # Step 6: Return the result
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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_98_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_indigenous_peoples_day(year):
    result = find_indigenous_peoples_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
