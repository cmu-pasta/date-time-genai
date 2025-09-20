
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def next_leap_year(dt: datetime) -> datetime:
    def is_leap_year(year: int) -> bool:
        # A year is a leap year if:
        # - It's divisible by 4, AND
        # - If it's divisible by 100, it must also be divisible by 400
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    
    # Start checking from the year after the given date's year
    year = dt.year + 1
    
    # Find the next leap year
    while not is_leap_year(year):
        year += 1
    
    # Return datetime object for January 1st of the next leap year
    return datetime(year, 1, 1)

# Entry point: next_leap_year(dt: datetime) -> datetime

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_3_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_next_leap_year(dt):
    result = next_leap_year(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
