
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def calculate_leap_years_between(start_year: int, end_year: int) -> int:
    # Ensure start_year is less than or equal to end_year
    if start_year > end_year:
        start_year, end_year = end_year, start_year
    
    leap_year_count = 0
    
    # Iterate through each year in the range (inclusive)
    for year in range(start_year, end_year + 1):
        # Check if the year is a leap year by trying to create February 29th
        try:
            date(year, 2, 29)  # If this succeeds, it's a leap year
            leap_year_count += 1
        except ValueError:
            # If ValueError is raised, February 29th doesn't exist, so not a leap year
            pass
    
    return leap_year_count

# Entry point: calculate_leap_years_between(start_year: int, end_year: int) -> int

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_27_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy())
def test_calculate_leap_years_between(start_year, end_year):
    result = calculate_leap_years_between(start_year, end_year)
    formatted_result = format_value_dt(result, start_year, end_year)
    log_file.write(formatted_result + "\n")
