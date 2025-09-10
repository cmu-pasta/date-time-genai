
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def is_palindrome_yyyymmdd(d: date) -> bool:
    """
    Helper function to check if the date in YYYYMMDD format is a palindrome.
    """
    yyyymmdd = d.strftime("%Y%m%d")
    return yyyymmdd == yyyymmdd[::-1]

def first_palindrome_date_after(start_date: date) -> date:
    """
    Finds the first date after the given date that is a palindrome in YYYYMMDD format.
    """
    current_date = start_date + timedelta(days=1)
    while True:
        if is_palindrome_yyyymmdd(current_date):
            return current_date
        current_date += timedelta(days=1)

# Entry point: first_palindrome_date_after(start_date: date) -> date

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_50txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_first_palindrome_date_after(start_date):
    result = first_palindrome_date_after(start_date)
    formatted_result = format_value_dt(result, start_date)
    log_file.write(formatted_result + "\n")
