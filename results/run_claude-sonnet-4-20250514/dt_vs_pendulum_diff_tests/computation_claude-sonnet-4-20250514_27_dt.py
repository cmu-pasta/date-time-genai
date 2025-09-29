
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date
def calculate_leap_years_between(year1: int, year2: int) -> int:
    # Ensure we have the correct start and end years
    start_year = min(year1, year2)
    end_year = max(year1, year2)
    
    leap_year_count = 0
    
    # Check each year in the range (inclusive)
    for year in range(start_year, end_year + 1):
        # Try to create February 29th for this year
        # If successful, it's a leap year
        try:
            date(year, 2, 29)
            leap_year_count += 1
        except ValueError:
            # February 29th doesn't exist for this year, so it's not a leap year
            continue
    
    return leap_year_count

# Entry point: calculate_leap_years_between(year1: int, year2: int) -> int

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_27_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy())
def test_calculate_leap_years_between(year1, year2):
    result = calculate_leap_years_between(year1, year2)
    formatted_result = format_value_dt(result, year1, year2)
    log_file.write(formatted_result + "\n")
