
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_next_matching_mmdd(start_date: date, month: int, day: int) -> date:
    # Step 1: Try to create the candidate date in the current year
    year = start_date.year
    while True:
        try:
            candidate = date(year, month, day)
            if candidate >= start_date:
                return candidate
            year += 1
        except ValueError:
            # Invalid date for this year (e.g., Feb 29 in non-leap years)
            year += 1

# Entry point: find_next_matching_mmdd(start_date: date, month: int, day: int) -> date

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_68txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), timestamp_strategy(), timestamp_strategy())
def test_find_next_matching_mmdd(start_date, month, day):
    result = find_next_matching_mmdd(start_date, month, day)
    formatted_result = format_value_dt(result, start_date, month, day)
    log_file.write(formatted_result + "\n")
