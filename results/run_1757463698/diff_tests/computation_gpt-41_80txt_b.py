
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def nth_previous_business_day(input_date: date, n: int) -> date:
    # Step 1: Validate that n is a positive integer
    if n < 1:
        raise ValueError("n must be at least 1")
    
    # Step 2: Start at the day before input_date and look for business days
    business_days_counted = 0
    current_date = input_date
    while business_days_counted < n:
        current_date -= timedelta(days=1)
        # Weekdays: Monday == 0 ... Sunday == 6
        if current_date.weekday() < 5:  # 0 (Monday) to 4 (Friday)
            business_days_counted += 1
    return current_date

# Entry point: nth_previous_business_day(input_date: date, n: int) -> date

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_80txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), timestamp_strategy())
def test_nth_previous_business_day(input_date, n):
    result = nth_previous_business_day(input_date, n)
    formatted_result = format_value_dt(result, input_date, n)
    log_file.write(formatted_result + "\n")
