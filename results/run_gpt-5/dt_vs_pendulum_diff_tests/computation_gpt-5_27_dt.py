
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def count_leap_years_between(year1: int, year2: int) -> int:
    """
    Count the number of leap years between two years, inclusive of both endpoints.
    Uses datetime.date to determine if Feb 29 exists for a given year.
    """
    # Normalize the range to be inclusive from the smaller to the larger year
    start_year = year1 if year1 <= year2 else year2
    end_year = year2 if year2 >= year1 else year1

    count = 0
    for y in range(start_year, end_year + 1):
        try:
            # If Feb 29 exists, it's a leap year
            date(y, 2, 29)
            count += 1
        except ValueError:
            # Not a leap year
            pass

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_27_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy())
def test_count_leap_years_between(year1, year2):
    result = count_leap_years_between(year1, year2)
    formatted_result = format_value_dt(result, year1, year2)
    log_file.write(formatted_result + "\n")
