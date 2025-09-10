
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def count_leap_years_in_range(start_date: date, end_date: date) -> int:
    # Step 1: Identify the range of years to consider (inclusive)
    start_year = start_date.year
    end_year = end_date.year
    
    # Step 2: Initialize the leap year counter
    leap_years_count = 0
    
    # Step 3: Iterate over each year in range and check leap year condition
    for year in range(start_year, end_year + 1):
        # Step 4: Check leap year rule
        if (year % 4 == 0) and ((year % 100 != 0) or (year % 400 == 0)):
            leap_years_count += 1
    
    # Step 5: Return the result as integer
    return leap_years_count

# Entry point: count_leap_years_in_range(start_date: date, end_date: date) -> int

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

if not os.path.exists(".logs/diff_test_logs"):
    os.makedirs(".logs/diff_test_logs")
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_22txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_count_leap_years_in_range(start_date, end_date):
    result = count_leap_years_in_range(start_date, end_date)
    formatted_result = format_value_dt(result, start_date, end_date)
    log_file.write(formatted_result + "\n")
