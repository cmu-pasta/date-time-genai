
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_indigenous_peoples_day(year: int) -> date:
    # Step 1: Get October 1st of the given year
    oct_first = date(year, 10, 1)
    
    # Step 2: Find what day of the week October 1st is (0=Monday, 6=Sunday)
    weekday = oct_first.weekday()
    
    # Step 3: Calculate days to add to reach the first Monday
    # If Oct 1st is Monday (0), we need 0 days
    # If Oct 1st is Tuesday (1), we need 6 days
    # If Oct 1st is Sunday (6), we need 1 day
    days_to_first_monday = (7 - weekday) % 7
    
    # Step 4: Calculate the second Monday (first Monday + 7 days)
    days_to_second_monday = days_to_first_monday + 7
    
    # Step 5: Return the date of the second Monday
    indigenous_peoples_day = oct_first + timedelta(days=days_to_second_monday)
    
    return indigenous_peoples_day

# Entry point: find_indigenous_peoples_day(year: int) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_98txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_find_indigenous_peoples_day(year):
    result = find_indigenous_peoples_day(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
