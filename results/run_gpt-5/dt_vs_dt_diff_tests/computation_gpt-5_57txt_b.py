
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def count_work_weeks_between(d1: date, d2: date) -> int:
    """
    Calculate the number of full work weeks (Mon-Fri, 5 days) between two dates.
    The interval is treated as half-open: [start, end), i.e., start is included and end is excluded.
    If d1 > d2, the dates are swapped.
    
    Args:
        d1: The first date.
        d2: The second date.
    Returns:
        The number of full work weeks (integer) between the two dates.
    """
    # Normalize order to ensure start <= end
    start = d1 if d1 <= d2 else d2
    end = d2 if d1 <= d2 else d1

    total_days = (end - start).days
    if total_days <= 0:
        return 0

    full_calendar_weeks = total_days // 7
    remainder_days = total_days % 7

    # Business days from full calendar weeks
    business_days = full_calendar_weeks * 5

    # Count weekday days in the remainder segment
    start_wd = start.weekday()  # 0=Mon .. 6=Sun
    extra_business = 0
    for i in range(remainder_days):
        if (start_wd + i) % 7 < 5:
            extra_business += 1

    business_days += extra_business

    # Number of full work weeks (5 business days per work week)
    work_weeks = business_days // 5
    return work_weeks

# Entry point: count_work_weeks_between(d1: date, d2: date) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_57txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_count_work_weeks_between(d1, d2):
    result = count_work_weeks_between(d1, d2)
    formatted_result = format_value_dt(result, d1, d2)
    log_file.write(formatted_result + "\n")
