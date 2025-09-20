
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_last_weekday_in_month(year: int, month: int, weekday: int) -> date:
    """
    Find the last occurrence of a specific weekday in a given month and year.

    Parameters:
    - year: int, e.g., 2025
    - month: int in 1..12
    - weekday: int where Monday=0, ..., Sunday=6 (as in datetime.date.weekday())

    Returns:
    - date: The date of the last occurrence of the specified weekday in the month.
    """
    if not (1 <= month <= 12):
        raise ValueError("month must be in 1..12")
    if not (0 <= weekday <= 6):
        raise ValueError("weekday must be in 0..6 (Monday=0 .. Sunday=6)")

    # Step 1: Find the first day of the next month
    if month == 12:
        first_of_next_month = date(year + 1, 1, 1)
    else:
        first_of_next_month = date(year, month + 1, 1)

    # Step 2: Last day of the current month
    last_of_month = first_of_next_month - timedelta(days=1)

    # Step 3: Compute offset back to the desired weekday
    offset_days = (last_of_month.weekday() - weekday) % 7

    # Step 4: Subtract offset to get the last occurrence
    target_date = last_of_month - timedelta(days=offset_days)
    return target_date

# Entry point: find_last_weekday_in_month(year: int, month: int, weekday: int) -> date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_80_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_find_last_weekday_in_month(year, month, weekday):
    result = find_last_weekday_in_month(year, month, weekday)
    formatted_result = format_value_dt(result, year, month, weekday)
    log_file.write(formatted_result + "\n")
