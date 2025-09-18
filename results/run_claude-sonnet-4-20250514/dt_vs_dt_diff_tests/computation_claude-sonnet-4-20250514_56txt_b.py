
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def find_next_valentines_day(given_date: date) -> date:
    # Step 1: Get the year from the given date
    current_year = given_date.year
    
    # Step 2: Create Valentine's Day for the current year (February 14th)
    valentines_this_year = date(current_year, 2, 14)
    
    # Step 3: Check if the given date is before Valentine's Day of this year
    if given_date < valentines_this_year:
        # If before, return this year's Valentine's Day
        return valentines_this_year
    else:
        # If on or after, return next year's Valentine's Day
        next_year = current_year + 1
        return date(next_year, 2, 14)

# Entry point: find_next_valentines_day(given_date: date) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_56txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_find_next_valentines_day(given_date):
    result = find_next_valentines_day(given_date)
    formatted_result = format_value_dt(result, given_date)
    log_file.write(formatted_result + "\n")
