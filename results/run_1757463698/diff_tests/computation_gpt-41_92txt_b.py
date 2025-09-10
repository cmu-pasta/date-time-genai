
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def same_weekday_next_year(given_date: date) -> date:
    # Step 1: Attempt to get the same month and day in the next year
    try:
        candidate = date(given_date.year + 1, given_date.month, given_date.day)
    except ValueError:
        # If invalid (like Feb 29 in a non-leap year), shift to March 1
        # This follows standard handling in datetime for leap years
        candidate = date(given_date.year + 1, 3, 1)
    
    # Step 2: Get the target weekday to match
    target_weekday = given_date.weekday()
    
    # Step 3: Find the next occurrence of this weekday >= candidate date
    days_difference = (target_weekday - candidate.weekday()) % 7
    result_date = candidate + timedelta(days=days_difference)
    
    # Step 4: Return the result
    return result_date

# Entry point: same_weekday_next_year(given_date: date) -> date

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_92txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_same_weekday_next_year(given_date):
    result = same_weekday_next_year(given_date)
    formatted_result = format_value_dt(result, given_date)
    log_file.write(formatted_result + "\n")
