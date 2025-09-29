
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def business_days_between(start: date, end: date) -> int:
    """
    Calculate the number of business days (Monday-Friday) between two dates.
    The calculation is exclusive of the end date and inclusive of the start date,
    matching the behavior of (end - start).days for total days.
    
    Args:
        start: The start date.
        end: The end date.
    Returns:
        The number of business days as an integer.
    """
    if start == end:
        return 0

    # Ensure start <= end
    if start > end:
        start, end = end, start

    total_days = (end - start).days  # end is exclusive
    full_weeks = total_days // 7
    business_days = full_weeks * 5

    remainder = total_days % 7
    start_weekday = start.weekday()  # 0=Mon, 6=Sun

    # Count weekdays in the remaining days
    for i in range(remainder):
        wd = (start_weekday + i) % 7
        if wd < 5:
            business_days += 1

    return business_days

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_0_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_business_days_between(start, end):
    result = business_days_between(start, end)
    formatted_result = format_value_dt(result, start, end)
    log_file.write(formatted_result + "\n")
