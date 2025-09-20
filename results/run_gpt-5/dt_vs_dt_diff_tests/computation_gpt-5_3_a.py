
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def next_leap_year_date(given_date: date) -> date:
    """
    Determine the next leap year after the given date and return the date of Feb 29 of that year.
    Raises ValueError if no such date exists within the supported datetime range.
    """
    year = given_date.year + 1

    # Python's datetime supports years in the range 1..9999
    while year <= 9999:
        # Leap year rule: divisible by 4 and (not divisible by 100 unless divisible by 400)
        if (year % 4 == 0) and ((year % 100 != 0) or (year % 400 == 0)):
            return date(year, 2, 29)
        year += 1

    # If we exceed 9999, we cannot represent the date in datetime.date
    raise ValueError("No representable next leap year exists after the given date.")

# Entry point: next_leap_year_date(given_date: date) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_3_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_next_leap_year_date(given_date):
    result = next_leap_year_date(given_date)
    formatted_result = format_value_dt(result, given_date)
    log_file.write(formatted_result + "\n")
