
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_last_weekday_in_month(month_date: datetime, target_weekday: int) -> datetime:
    # Get the year and month from the input date
    year = month_date.year
    month = month_date.month
    
    # Calculate the first day of the next month
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    
    # Get the last day of the current month
    last_day_of_month = next_month - timedelta(days=1)
    
    # Start from the last day and go backwards until we find the target weekday
    current_date = last_day_of_month
    while current_date.weekday() != target_weekday:
        current_date = current_date - timedelta(days=1)
    
    return current_date

# Entry point: find_last_weekday_in_month(month_date: datetime, target_weekday: int) -> datetime

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_80_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), timestamp_strategy())
def test_find_last_weekday_in_month(month_date, target_weekday):
    result = find_last_weekday_in_month(month_date, target_weekday)
    formatted_result = format_value_dt(result, month_date, target_weekday)
    log_file.write(formatted_result + "\n")
