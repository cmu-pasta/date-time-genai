
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def count_weekends_between(start: date, end: date) -> int:
    # Ensure start is not after end
    if start > end:
        start, end = end, start

    # Inclusive total days
    total_days = (end - start).days + 1

    # Weekend days from full weeks
    full_weeks = total_days // 7
    weekend_days = full_weeks * 2

    # Remaining days
    remainder = total_days % 7
    start_weekday = start.weekday()  # Monday=0, Sunday=6

    # Count weekend days in the remainder span
    for i in range(remainder):
        day_idx = (start_weekday + i) % 7
        if day_idx >= 5:  # 5=Saturday, 6=Sunday
            weekend_days += 1

    return weekend_days

# Entry point: count_weekends_between(start: date, end: date) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_15_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_count_weekends_between(start, end):
    result = count_weekends_between(start, end)
    formatted_result = format_value_dt(result, start, end)
    log_file.write(formatted_result + "\n")
