
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def last_business_day_of_month(given_date: date) -> date:
    # Step 1: Find the first day of the next month
    if given_date.month == 12:
        first_day_next_month = date(given_date.year + 1, 1, 1)
    else:
        first_day_next_month = date(given_date.year, given_date.month + 1, 1)
    
    # Step 2: Find the last day of the current month
    last_day_of_month = first_day_next_month - timedelta(days=1)
    
    # Step 3: Move backward until we find a business day (Monday-Friday)
    while last_day_of_month.weekday() >= 5:  # 5=Saturday, 6=Sunday
        last_day_of_month -= timedelta(days=1)
    
    # Step 4: Return the result
    return last_day_of_month

# Entry point: last_business_day_of_month(given_date: date) -> date

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_45txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_last_business_day_of_month(given_date):
    result = last_business_day_of_month(given_date)
    formatted_result = format_value_dt(result, given_date)
    log_file.write(formatted_result + "\n")
