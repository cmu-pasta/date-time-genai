
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def count_fridays_between(start_date: date, end_date: date) -> int:
    # Step 1: Ensure the start date is before or equal to the end date
    if start_date > end_date:
        start_date, end_date = end_date, start_date

    # Step 2: Find the first Friday on or after the start date
    days_until_friday = (4 - start_date.weekday()) % 7  # 4 means Friday
    first_friday = start_date + timedelta(days=days_until_friday)

    # Step 3: Initialize the Friday counter
    count = 0

    # Step 4: Count Fridays until exceeding end_date
    current_friday = first_friday
    while current_friday <= end_date:
        count += 1
        current_friday += timedelta(days=7)

    # Step 5: Return the number of Fridays found
    return count

# Entry point: count_fridays_between(start_date: date, end_date: date) -> int

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_81txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_count_fridays_between(start_date, end_date):
    result = count_fridays_between(start_date, end_date)
    formatted_result = format_value_dt(result, start_date, end_date)
    log_file.write(formatted_result + "\n")
