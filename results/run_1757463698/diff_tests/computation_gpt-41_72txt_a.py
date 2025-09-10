
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def count_weekend_days_in_month(year: int, month: int) -> int:
    # Step 1: Create a date object for the first day of the month
    first_day = date(year, month, 1)
    
    # Step 2: Calculate the first day of the next month
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)
    
    # Step 3: Find the number of days in the month
    days_in_month = (next_month - first_day).days
    
    # Step 4: Initialize the weekend counter
    weekend_count = 0
    
    # Step 5: Iterate through all the days in the month
    for day_delta in range(days_in_month):
        current_day = first_day + timedelta(days=day_delta)
        # Step 6: Check if the day is Saturday (5) or Sunday (6)
        if current_day.weekday() == 5 or current_day.weekday() == 6:
            weekend_count += 1
    
    # Step 7: Return the result
    return weekend_count

# Entry point: count_weekend_days_in_month(year: int, month: int) -> int

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

if not os.path.exists(".logs/diff_test_logs"):
    os.makedirs(".logs/diff_test_logs")
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_72txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy())
def test_count_weekend_days_in_month(year, month):
    result = count_weekend_days_in_month(year, month)
    formatted_result = format_value_dt(result, year, month)
    log_file.write(formatted_result + "\n")
