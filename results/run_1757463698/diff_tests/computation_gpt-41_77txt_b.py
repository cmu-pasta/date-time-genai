
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
import calendar
def count_weekday_in_month(year: int, month: int, weekday: int) -> int:
    # Step 1: Get the total number of days in the given month
    _, num_days = calendar.monthrange(year, month)
    
    # Step 2: Initialize a counter for matching weekdays
    count = 0
    
    # Step 3: Loop through each day of the month
    for day in range(1, num_days + 1):
        current_date = date(year, month, day)
        if current_date.weekday() == weekday:
            count += 1
    
    # Step 4: Return the total count
    return count

# Entry point: count_weekday_in_month(year: int, month: int, weekday: int) -> int

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_77txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_count_weekday_in_month(year, month, weekday):
    result = count_weekday_in_month(year, month, weekday)
    formatted_result = format_value_dt(result, year, month, weekday)
    log_file.write(formatted_result + "\n")
