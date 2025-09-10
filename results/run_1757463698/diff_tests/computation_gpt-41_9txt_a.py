
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def last_day_of_month(given_date: date) -> date:
    # Step 1: Determine the year and month for the next month
    if given_date.month == 12:
        next_month = 1
        next_year = given_date.year + 1
    else:
        next_month = given_date.month + 1
        next_year = given_date.year
    
    # Step 2: Create the first day of the next month
    first_day_next_month = date(next_year, next_month, 1)
    
    # Step 3: Subtract one day to get the last day of the current month
    last_day = first_day_next_month - timedelta(days=1)
    
    # Step 4: Return the result
    return last_day

# Entry point: last_day_of_month(given_date: date) -> date

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_9txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_last_day_of_month(given_date):
    result = last_day_of_month(given_date)
    formatted_result = format_value_dt(result, given_date)
    log_file.write(formatted_result + "\n")
