
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def find_next_matching_mmdd(start_date: date, month: int, day: int) -> date:
    """
    Given a start date, find the next occurrence (after start_date) of the date 
    with the specified MM-DD (month and day pattern).

    Args:
        start_date (date): The date to start searching from (exclusive).
        month (int): Month of the target pattern (1-12).
        day (int): Day of the target pattern (1-31, must be valid for the month).

    Returns:
        date: The next date after start_date with the given MM-DD.
    """
    year = start_date.year

    while True:
        try:
            candidate = date(year, month, day)
            if candidate > start_date:
                return candidate
        except ValueError:
            # The date is invalid for the current year (e.g., Feb 29 in a non-leap year)
            pass
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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_68txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), timestamp_strategy(), timestamp_strategy())
def test_find_next_matching_mmdd(start_date, month, day):
    result = find_next_matching_mmdd(start_date, month, day)
    formatted_result = format_value_dt(result, start_date, month, day)
    log_file.write(formatted_result + "\n")
