
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, datetime
def _is_leap_year(year: int) -> bool:
    """Return True if the given Gregorian year is a leap year."""
    return (year % 4 == 0) and (year % 100 != 0 or year % 400 == 0)

def next_leap_year_after(given_date: date) -> int:
    """
    Determine the next leap year strictly after the given date.
    Accepts a datetime.date (a datetime.datetime is also acceptable since it subclasses date).
    Returns the year as an integer.
    """
    year = given_date.year + 1
    while not _is_leap_year(year):
        year += 1
    return year

# Entry point: next_leap_year_after(given_date: date) -> int

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

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_3txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_next_leap_year_after(given_date):
    result = next_leap_year_after(given_date)
    formatted_result = format_value_dt(result, given_date)
    log_file.write(formatted_result + "\n")
