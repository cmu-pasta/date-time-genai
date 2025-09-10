
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def calculate_weekdays_between(d1: date, d2: date) -> int:
    # Step 1: Ensure start_date is not after end_date
    start_date = min(d1, d2)
    end_date = max(d1, d2)
    
    # Step 2: Initialize weekday counter
    weekday_count = 0

    # Step 3: Iterate from start_date to end_date (exclusive)
    current_date = start_date
    while current_date < end_date:
        # Step 4: Check if the current day is a weekday (Monday=0 ... Friday=4)
        if current_date.weekday() < 5:
            weekday_count += 1
        current_date += timedelta(days=1)
    
    # Step 5: Return the number of weekdays
    return weekday_count

# Entry point: calculate_weekdays_between(d1: date, d2: date) -> int

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_0txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_calculate_weekdays_between(d1, d2):
    result = calculate_weekdays_between(d1, d2)
    formatted_result = format_value_dt(result, d1, d2)
    log_file.write(formatted_result + "\n")
