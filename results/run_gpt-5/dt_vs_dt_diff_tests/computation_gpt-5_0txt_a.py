
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def calculate_business_days(start: date, end: date) -> int:
    """
    Calculate the number of business days (Monday-Friday) between two dates, inclusive.
    If the start date is after the end date, the dates are swapped.
    """
    # Step 1: Ensure start <= end
    if start > end:
        start, end = end, start

    # Step 2: Total days inclusive
    total_days = (end - start).days + 1  # inclusive of both endpoints

    # Step 3: Whole weeks contribute 5 business days each
    full_weeks = total_days // 7
    business_days = full_weeks * 5

    # Step 4: Handle the remaining days (at most 6)
    remaining_days = total_days % 7
    start_weekday = start.weekday()  # Monday=0 ... Sunday=6

    # Count weekdays in the remainder span
    for i in range(remaining_days):
        weekday = (start_weekday + i) % 7
        if weekday < 5:  # Monday-Friday
            business_days += 1

    return business_days

# Entry point: calculate_business_days(start: date, end: date) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_0txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_calculate_business_days(start, end):
    result = calculate_business_days(start, end)
    formatted_result = format_value_dt(result, start, end)
    log_file.write(formatted_result + "\n")
