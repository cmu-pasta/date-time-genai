
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def add_business_days(start: date, n: int) -> date:
    """
    Return the date that is exactly n business days after the given start date.
    - Business days are Monday (0) through Friday (4); weekends are Saturday (5) and Sunday (6).
    - If n == 0, the start date is returned unchanged, even if it is a weekend.
    - Supports negative n to move backward by business days.
    """
    if n == 0:
        return start

    wd = start.weekday()  # Monday=0 ... Sunday=6
    current = start

    if n > 0:
        # If starting on a weekend, move forward to Monday without consuming a business day
        if wd >= 5:
            current += timedelta(days=(7 - wd))  # to Monday
        # Add whole business weeks
        weeks = n // 5
        current += timedelta(days=weeks * 7)
        rem = n % 5
        if rem == 0:
            return current
        # Add remaining business days, skipping weekend if needed
        w = current.weekday()  # should be 0..4
        add_days = rem + (2 if w + rem > 4 else 0)
        return current + timedelta(days=add_days)

    else:  # n < 0
        k = -n
        # If starting on a weekend, move backward to Friday without consuming a business day
        if wd >= 5:
            current -= timedelta(days=(wd - 4))  # to Friday
        # Subtract whole business weeks
        weeks = k // 5
        current -= timedelta(days=weeks * 7)
        rem = k % 5
        if rem == 0:
            return current
        # Subtract remaining business days, skipping weekend if needed
        w = current.weekday()  # 0..4
        sub_days = rem + (2 if w - rem < 0 else 0)
        return current - timedelta(days=sub_days)

# Entry point: add_business_days(start: date, n: int) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_14txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), timestamp_strategy())
def test_add_business_days(start, n):
    result = add_business_days(start, n)
    formatted_result = format_value_dt(result, start, n)
    log_file.write(formatted_result + "\n")
