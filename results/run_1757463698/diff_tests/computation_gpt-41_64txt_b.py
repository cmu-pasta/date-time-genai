
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def count_fridays_the_13th(year: int) -> int:
    # Step 1: Initialize counter
    count = 0
    # Step 2: Loop through all months
    for month in range(1, 13):
        thirteenth = date(year, month, 13)
        # Step 3: Check if 13th day is a Friday (weekday() == 4)
        if thirteenth.weekday() == 4:
            count += 1
    # Step 4: Return count of Fridays the 13th
    return count

# Entry point: count_fridays_the_13th(year: int) -> int

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_64txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_count_fridays_the_13th(year):
    result = count_fridays_the_13th(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
