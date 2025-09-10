
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def add_business_days(start_date: date, business_days: int) -> date:
    # Step 1: Initialize count and current date
    current_date = start_date
    days_added = 0

    # Step 2: Add business days, skipping weekends
    while days_added < business_days:
        current_date += timedelta(days=1)
        # Step 3: Check if it's a weekday (Monday=0 to Friday=4)
        if current_date.weekday() < 5:
            days_added += 1

    # Step 4: Return the final date
    return current_date

# Entry point: add_business_days(start_date: date, business_days: int) -> date

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_7txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), timestamp_strategy())
def test_add_business_days(start_date, business_days):
    result = add_business_days(start_date, business_days)
    formatted_result = format_value_dt(result, start_date, business_days)
    log_file.write(formatted_result + "\n")
