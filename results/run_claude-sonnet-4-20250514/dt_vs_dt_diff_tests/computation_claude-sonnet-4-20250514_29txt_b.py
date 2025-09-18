
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def find_thanksgiving_date(year: int) -> date:
    # Step 1: Create November 1st of the given year
    november_first = date(year, 11, 1)
    
    # Step 2: Find the weekday of November 1st (0=Monday, 6=Sunday)
    november_first_weekday = november_first.weekday()
    
    # Step 3: Calculate days to add to reach the first Thursday (weekday 3)
    # If November 1st is already a Thursday, we add 0 days
    # Otherwise, we calculate the difference
    days_to_first_thursday = (3 - november_first_weekday) % 7
    
    # Step 4: Get the first Thursday of November
    first_thursday = november_first + timedelta(days=days_to_first_thursday)
    
    # Step 5: Add 21 days (3 weeks) to get the fourth Thursday
    thanksgiving_date = first_thursday + timedelta(days=21)
    
    return thanksgiving_date

# Entry point: find_thanksgiving_date(year: int) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_29txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_thanksgiving_date(year):
    result = find_thanksgiving_date(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
