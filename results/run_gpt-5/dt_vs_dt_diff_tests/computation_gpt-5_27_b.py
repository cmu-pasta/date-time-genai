
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def count_leap_years_between(year1: int, year2: int) -> int:
    """
    Count the number of leap years between two years, inclusive.
    A year is considered leap if February 29 exists for that year.
    """
    # Ensure start_year <= end_year without using tuples
    if year1 <= year2:
        start_year = year1
        end_year = year2
    else:
        start_year = year2
        end_year = year1

    count = 0
    year = start_year
    while year <= end_year:
        try:
            # If this succeeds, the year is a leap year
            datetime(year, 2, 29)
            count += 1
        except ValueError:
            # Not a leap year
            pass
        year += 1

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_27_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy())
def test_count_leap_years_between(year1, year2):
    result = count_leap_years_between(year1, year2)
    formatted_result = format_value_dt(result, year1, year2)
    log_file.write(formatted_result + "\n")
