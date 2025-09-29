
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, datetime
def _is_leap_year(year: int) -> bool:
    """
    Determine if a given year is a leap year using the datetime module.
    Returns True if Feb 29 exists for the year; otherwise False.
    """
    try:
        datetime(year, 2, 29)
        return True
    except ValueError:
        return False

def next_leap_year_after(d: date) -> int:
    """
    Given a date, determine the next leap year strictly after the year of the given date.
    For example, if d is in 2024, the function returns 2028 (not 2024).
    """
    year = d.year + 1
    while not _is_leap_year(year):
        year += 1
    return year

# Entry point: next_leap_year_after(d: date) -> int

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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_3txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_next_leap_year_after(d):
    result = next_leap_year_after(d)
    formatted_result = format_value_dt(result, d)
    log_file.write(formatted_result + "\n")
