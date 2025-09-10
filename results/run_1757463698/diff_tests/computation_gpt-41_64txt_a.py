
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def is_friday_the_13th(year: int, month: int) -> bool:
    """
    Returns True if the given year and month have Friday the 13th, False otherwise.
    """
    d = date(year, month, 13)
    return d.weekday() == 4

def next_friday_the_13th(year: int, last_month_checked: int) -> date:
    """
    Returns the next Friday the 13th date object for a given year, after last_month_checked.
    Returns None if none remain.
    """
    for month in range(last_month_checked + 1, 13):
        if is_friday_the_13th(year, month):
            return date(year, month, 13)
    return None

# Entry point: next_friday_the_13th(year: int, last_month_checked: int) -> date

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_64txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy())
def test_next_friday_the_13th(year, last_month_checked):
    result = next_friday_the_13th(year, last_month_checked)
    formatted_result = format_value_dt(result, year, last_month_checked)
    log_file.write(formatted_result + "\n")
