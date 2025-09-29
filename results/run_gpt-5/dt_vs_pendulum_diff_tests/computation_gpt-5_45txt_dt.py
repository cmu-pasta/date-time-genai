
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def business_days_remaining_in_month(d: date) -> int:
    """
    Calculate the number of business days (Monday-Friday) remaining in the current month
    for the given date, inclusive of the given date if it is a business day.
    """
    # Step 1: Find the first day of the next month
    if d.month == 12:
        first_next_month = date(d.year + 1, 1, 1)
    else:
        first_next_month = date(d.year, d.month + 1, 1)
    
    # Step 2: Compute the last day of the current month
    last_day_current_month = first_next_month - timedelta(days=1)
    
    # Step 3: Iterate from given date to last day of month and count business days
    current = d
    business_days = 0
    one_day = timedelta(days=1)
    while current <= last_day_current_month:
        if current.weekday() < 5:  # 0=Monday, ..., 6=Sunday
            business_days += 1
        current += one_day
    
    # Step 4: Return the count
    return business_days

# Entry point: business_days_remaining_in_month(d: date) -> int

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

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_45txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_business_days_remaining_in_month(d):
    result = business_days_remaining_in_month(d)
    formatted_result = format_value_dt(result, d)
    log_file.write(formatted_result + "\n")
