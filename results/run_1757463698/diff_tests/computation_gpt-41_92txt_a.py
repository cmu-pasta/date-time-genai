
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def next_year_same_weekday(input_date: date) -> date:
    # Step 1: Try to create a date in the next year with the same month and day.
    try:
        candidate = date(input_date.year + 1, input_date.month, input_date.day)
    except ValueError:
        # Handles cases like February 29th not existing in non-leap years.
        # Move to March 1st (or the next valid date).
        next_month = input_date.month + 1 if input_date.month < 12 else 1
        next_year = input_date.year + 1 if input_date.month < 12 else input_date.year + 1
        candidate = date(next_year, next_month, 1)

    # Step 2: Find and return the earliest date >= candidate with the same weekday as input_date.
    target_weekday = input_date.weekday()
    while candidate.weekday() != target_weekday:
        candidate += timedelta(days=1)
    return candidate

# Entry point: next_year_same_weekday(input_date: date) -> date

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_92txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_next_year_same_weekday(input_date):
    result = next_year_same_weekday(input_date)
    formatted_result = format_value_dt(result, input_date)
    log_file.write(formatted_result + "\n")
