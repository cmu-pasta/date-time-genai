
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def find_last_weekday_in_month(year: int, month: int, target_weekday: int) -> date:
    # Step 1: Find the last day of the given month
    if month == 12:
        # If December, next month is January of next year
        next_month_first = date(year + 1, 1, 1)
    else:
        # Otherwise, go to first day of next month
        next_month_first = date(year, month + 1, 1)
    
    # Last day of current month is one day before first day of next month
    last_day_of_month = next_month_first - timedelta(days=1)
    
    # Step 2: Work backwards from last day until we find the target weekday
    current_day = last_day_of_month
    while current_day.weekday() != target_weekday:
        current_day = current_day - timedelta(days=1)
    
    # Step 3: Return the date of the last occurrence
    return current_day

# Entry point: find_last_weekday_in_month(year: int, month: int, target_weekday: int) -> date

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_80_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_find_last_weekday_in_month(year, month, target_weekday):
    result = find_last_weekday_in_month(year, month, target_weekday)
    formatted_result = format_value_dt(result, year, month, target_weekday)
    log_file.write(formatted_result + "\n")
