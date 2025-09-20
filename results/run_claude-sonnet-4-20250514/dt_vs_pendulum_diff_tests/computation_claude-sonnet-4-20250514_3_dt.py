
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def find_next_leap_year(dt: datetime) -> datetime:
    def is_leap_year(year: int) -> bool:
        # A year is a leap year if:
        # - It's divisible by 400, OR
        # - It's divisible by 4 AND not divisible by 100
        return (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)
    
    # Start checking from the next year after the given date's year
    current_year = dt.year + 1
    
    # Find the next leap year
    while not is_leap_year(current_year):
        current_year += 1
    
    # Return January 1st of the next leap year
    return datetime(current_year, 1, 1)

# Entry point: find_next_leap_year(dt: datetime) -> datetime

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_3_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_next_leap_year(dt):
    result = find_next_leap_year(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
