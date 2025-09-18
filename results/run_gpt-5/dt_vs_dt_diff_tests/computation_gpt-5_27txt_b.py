
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def count_leap_years_between(year1: int, year2: int) -> int:
    """
    Calculate the number of leap years between two years (inclusive of both endpoints).

    Args:
        year1: An integer year within the supported datetime range [1, 9999].
        year2: An integer year within the supported datetime range [1, 9999].

    Returns:
        An integer count of leap years between the two years, inclusive.
    """
    # Validate input years using datetime.date bounds
    min_year, max_year = date.min.year, date.max.year
    if not (min_year <= year1 <= max_year) or not (min_year <= year2 <= max_year):
        raise ValueError(f"Years must be in the range [{min_year}, {max_year}].")

    # Ensure a <= b for the inclusive range [a, b]
    a, b = (year1, year2) if year1 <= year2 else (year2, year1)

    # Helper: number of leap years from year 1 up to and including y
    def _leaps_up_to(y: int) -> int:
        return (y // 4) - (y // 100) + (y // 400)

    # Inclusive count in [a, b]
    return _leaps_up_to(b) - _leaps_up_to(a - 1)

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_27txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy())
def test_count_leap_years_between(year1, year2):
    result = count_leap_years_between(year1, year2)
    formatted_result = format_value_dt(result, year1, year2)
    log_file.write(formatted_result + "\n")
