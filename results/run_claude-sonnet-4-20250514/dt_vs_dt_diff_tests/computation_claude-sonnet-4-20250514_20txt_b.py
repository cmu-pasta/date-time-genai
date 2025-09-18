
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_previous_friday(given_date: date) -> date:
    # Step 1: Get the weekday of the given date (Monday=0, Friday=4)
    weekday = given_date.weekday()
    
    # Step 2: Calculate how many days back to go to reach the previous Friday
    days_back = (weekday - 4) % 7
    
    # Step 3: Handle special case - if given date is Friday, go back 7 days
    if days_back == 0:
        days_back = 7
    
    # Step 4: Calculate the previous Friday by subtracting the required days
    previous_friday = given_date - timedelta(days=days_back)
    
    # Step 5: Return the result
    return previous_friday

# Entry point: find_previous_friday(given_date: date) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_20txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_find_previous_friday(given_date):
    result = find_previous_friday(given_date)
    formatted_result = format_value_dt(result, given_date)
    log_file.write(formatted_result + "\n")
