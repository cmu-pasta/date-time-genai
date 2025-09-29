
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def business_days_between(start: date, end: date) -> int:
    """
    Calculate the number of business days (Monday-Friday) between two dates, inclusive.
    If start > end, the dates are swapped.
    No holidays are considered.
    """
    # Step 1: Normalize order so start <= end
    if start > end:
        start, end = end, start

    # Step 2: Compute total span in days, inclusive of both endpoints
    total_days_inclusive = (end - start).days + 1

    # Step 3: Count full weeks and remaining days
    full_weeks = total_days_inclusive // 7
    remaining_days = total_days_inclusive % 7

    # Each full week has 5 business days (Mon-Fri)
    business_days = full_weeks * 5

    # Step 4: Count business days in the remaining partial week starting from 'start'
    start_weekday = start.weekday()  # 0=Mon, ..., 6=Sun
    extra = 0
    for i in range(remaining_days):
        weekday = (start_weekday + i) % 7
        if weekday < 5:  # Monday-Friday
            extra += 1

    return business_days + extra

# Entry point: business_days_between(start: date, end: date) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_0txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_business_days_between(start, end):
    result = business_days_between(start, end)
    formatted_result = format_value_dt(result, start, end)
    log_file.write(formatted_result + "\n")
