
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_leap_years_between(year1: int, year2: int) -> int:
    # Ensure year1 is the smaller year for proper range calculation
    start_year = min(year1, year2)
    end_year = max(year1, year2)
    
    leap_year_count = 0
    
    # Iterate through all years in the range (inclusive)
    for year in range(start_year, end_year + 1):
        # Check if the year is a leap year
        if is_leap_year(year):
            leap_year_count += 1
    
    return leap_year_count

def is_leap_year(year: int) -> bool:
    # A year is a leap year if:
    # 1. It's divisible by 4
    # 2. If divisible by 100, it must also be divisible by 400
    if year % 4 == 0:
        if year % 100 == 0:
            return year % 400 == 0
        return True
    return False

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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_27txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy())
def test_calculate_leap_years_between(year1, year2):
    result = calculate_leap_years_between(year1, year2)
    formatted_result = format_value_dt(result, year1, year2)
    log_file.write(formatted_result + "\n")
