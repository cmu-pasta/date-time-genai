
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def add_business_days(start_date: date, n: int) -> date:
    if n < 0:
        raise ValueError("n must be a non-negative integer representing business days to add.")
    if n == 0:
        return start_date

    current = start_date
    days_added = 0
    one_day = timedelta(days=1)

    while days_added < n:
        current += one_day
        if current.weekday() < 5:  # Monday=0, ..., Friday=4 are business days
            days_added += 1

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_14_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), timestamp_strategy())
def test_add_business_days(start_date, n):
    result = add_business_days(start_date, n)
    formatted_result = format_value_dt(result, start_date, n)
    log_file.write(formatted_result + "\n")
