
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def add_business_days(start_date: date, n: int) -> date:
    """
    Return the date that is exactly n business days after start_date.
    - Business days are Monday (0) through Friday (4).
    - If n is 0, returns start_date.
    - Supports negative n to move backward in business days.
    """
    if n == 0:
        return start_date

    step = 1 if n > 0 else -1
    remaining = abs(n)
    current = start_date

    while remaining > 0:
        current += timedelta(days=step)
        if 0 <= current.weekday() <= 4:  # Monday=0, Sunday=6
            remaining -= 1

    return current

# Entry point: add_business_days(start_date: date, n: int) -> date

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_14txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), timestamp_strategy())
def test_add_business_days(start_date, n):
    result = add_business_days(start_date, n)
    formatted_result = format_value_dt(result, start_date, n)
    log_file.write(formatted_result + "\n")
