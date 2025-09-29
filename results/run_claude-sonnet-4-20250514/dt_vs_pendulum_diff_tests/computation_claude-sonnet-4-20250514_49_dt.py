
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def count_sundays_in_february(year: int) -> int:
    # Determine the number of days in February for the given year
    # Check if it's a leap year
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        days_in_february = 29
    else:
        days_in_february = 28
    
    sunday_count = 0
    
    # Loop through each day in February
    for day in range(1, days_in_february + 1):
        date = datetime(year, 2, day)
        # Check if it's a Sunday (weekday() returns 6 for Sunday)
        if date.weekday() == 6:
            sunday_count += 1
    
    return sunday_count

# Entry point: count_sundays_in_february(year: int) -> int

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_49_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_count_sundays_in_february(year):
    result = count_sundays_in_february(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
