
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def _is_leap_year(year: int) -> bool:
    """
    Determine if a given year is a leap year using the datetime library
    by checking if February 29 exists for that year.

    Raises:
        ValueError: If year is outside the supported datetime range [1, 9999].
    """
    if not (1 <= year <= 9999):
        raise ValueError("Year must be in the range 1..9999 for datetime.date.")
    try:
        date(year, 2, 29)
        return True
    except ValueError:
        return False

def count_leap_years_between(year1: int, year2: int) -> int:
    """
    Calculate the number of leap years between two years (inclusive of both endpoints).

    Args:
        year1: An integer year in the range 1..9999.
        year2: An integer year in the range 1..9999.

    Returns:
        An integer count of leap years between year1 and year2, inclusive.

    Raises:
        ValueError: If either year is outside the supported datetime range [1, 9999].
    """
    start = min(year1, year2)
    end = max(year1, year2)

    if not (1 <= start <= 9999) or not (1 <= end <= 9999):
        raise ValueError("Years must be in the range 1..9999 for datetime.date.")

    count = 0
    for y in range(start, end + 1):
        if _is_leap_year(y):
            count += 1
    return count

# Entry point: count_leap_years_between(year1: int, year2: int) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_27txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy())
def test_count_leap_years_between(year1, year2):
    result = count_leap_years_between(year1, year2)
    formatted_result = format_value_dt(result, year1, year2)
    log_file.write(formatted_result + "\n")
