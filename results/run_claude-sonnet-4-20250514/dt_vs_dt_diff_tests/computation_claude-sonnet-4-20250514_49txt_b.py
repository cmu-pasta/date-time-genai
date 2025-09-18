
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def count_sundays_in_february(year: int) -> int:
    # Step 1: Create the first day of February for the given year
    first_day = datetime(year, 2, 1)
    
    # Step 2: Create the first day of March to find the end of February
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        # Leap year - February has 29 days
        last_day = datetime(year, 2, 29)
    else:
        # Regular year - February has 28 days
        last_day = datetime(year, 2, 28)
    
    # Step 3: Count Sundays in February
    sunday_count = 0
    current_day = first_day
    
    while current_day <= last_day:
        # Check if current day is Sunday (weekday() returns 6 for Sunday)
        if current_day.weekday() == 6:
            sunday_count += 1
        # Move to next day
        current_day += timedelta(days=1)
    
    # Step 4: Return the count of Sundays
    return sunday_count

# Entry point: count_sundays_in_february(year: int) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_49txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_count_sundays_in_february(year):
    result = count_sundays_in_february(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
