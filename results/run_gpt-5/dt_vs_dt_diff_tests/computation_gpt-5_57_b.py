
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def calculate_work_weeks_between(start: date, end: date) -> int:
    # Ensure chronological order
    if end < start:
        start, end = end, start

    # Total days between dates, end-exclusive
    total_days = (end - start).days

    # Full weeks and remainder days
    full_weeks = total_days // 7
    remainder_days = total_days % 7

    # Weekdays contributed by full weeks
    weekdays = full_weeks * 5

    # Add weekdays from the remainder span
    start_wd = start.weekday()  # Monday=0 ... Sunday=6
    i = 0
    while i < remainder_days:
        if (start_wd + i) % 7 < 5:  # Mon-Fri are < 5
            weekdays += 1
        i += 1

    # Number of full work weeks (each work week has 5 weekdays)
    work_weeks = weekdays // 5
    return work_weeks

# Entry point: calculate_work_weeks_between(start: date, end: date) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_57_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_calculate_work_weeks_between(start, end):
    result = calculate_work_weeks_between(start, end)
    formatted_result = format_value_dt(result, start, end)
    log_file.write(formatted_result + "\n")
