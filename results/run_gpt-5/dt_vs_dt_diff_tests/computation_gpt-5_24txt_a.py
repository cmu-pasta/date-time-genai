
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def calculate_working_hours_between(start: datetime, end: datetime) -> timedelta:
    # Ensure start <= end
    if end < start:
        start, end = end, start

    # If equal, zero duration
    if start == end:
        return timedelta(0)

    # Helper to check weekday (Mon-Fri)
    def is_weekday(d: datetime) -> bool:
        return d.weekday() < 5  # Monday=0, Sunday=6

    # If within the same calendar day
    if start.date() == end.date():
        return (end - start) if is_weekday(start) else timedelta(0)

    total = timedelta(0)

    # First day contribution
    start_day_end = datetime(start.year, start.month, start.day) + timedelta(days=1)
    if is_weekday(start):
        total += (start_day_end - start)

    # Middle full days
    current = start_day_end
    end_day_start = datetime(end.year, end.month, end.day)
    while current < end_day_start:
        if is_weekday(current):
            total += timedelta(days=1)
        current += timedelta(days=1)

    # Last day contribution
    if is_weekday(end):
        total += (end - end_day_start)

    return total

# Entry point: calculate_working_hours_between(start: datetime, end: datetime) -> timedelta

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_24txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_working_hours_between(start, end):
    result = calculate_working_hours_between(start, end)
    formatted_result = format_value_dt(result, start, end)
    log_file.write(formatted_result + "\n")
