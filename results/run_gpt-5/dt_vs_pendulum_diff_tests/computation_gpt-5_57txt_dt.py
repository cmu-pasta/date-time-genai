
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def calculate_work_weeks_between(start: date, end: date) -> int:
    """
    Calculate the number of full work weeks (Mon-Fri) between two dates.
    The interval is half-open: [start, end), meaning the end date is not included.
    A work week consists of 5 weekdays (Monday through Friday).
    """
    # Step 1: Normalize order to ensure start <= end
    if start > end:
        start, end = end, start

    # Step 2: Compute the total days in the half-open interval [start, end)
    total_days = (end - start).days
    if total_days <= 0:
        return 0

    # Step 3: Compute weekdays contributed by complete weeks
    full_weeks = total_days // 7
    weekdays = full_weeks * 5

    # Step 4: Handle the remaining days to count additional weekdays
    remaining_days = total_days % 7
    start_weekday = start.weekday()  # 0=Mon, 6=Sun

    # Count weekdays in the remaining span
    extra_weekdays = 0
    for i in range(remaining_days):
        dow = (start_weekday + i) % 7
        if dow < 5:  # Monday-Friday
            extra_weekdays += 1

    weekdays += extra_weekdays

    # Step 5: Convert total weekdays to number of full work weeks
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

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_57txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_calculate_work_weeks_between(start, end):
    result = calculate_work_weeks_between(start, end)
    formatted_result = format_value_dt(result, start, end)
    log_file.write(formatted_result + "\n")
