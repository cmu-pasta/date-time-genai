
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_nth_weekday_occurrence(month_date: datetime, weekday: int, n: int) -> datetime:
    # Get the year and month from the input date
    year = month_date.year
    month = month_date.month
    
    # Start from the first day of the month
    current_date = datetime(year, month, 1)
    
    count = 0
    
    # Iterate through the days of the month
    while current_date.month == month:
        # Check if this day is the target weekday (0=Monday, 6=Sunday)
        if current_date.weekday() == weekday:
            count += 1
            if count == n:
                return current_date
        
        # Move to the next day
        current_date += timedelta(days=1)
    
    # If nth occurrence doesn't exist, return the first day of the month
    # (This assumes valid input where nth occurrence exists)
    return datetime(year, month, 1)

# Entry point: find_nth_weekday_occurrence(month_date: datetime, weekday: int, n: int) -> datetime

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_17_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), timestamp_strategy(), timestamp_strategy())
def test_find_nth_weekday_occurrence(month_date, weekday, n):
    result = find_nth_weekday_occurrence(month_date, weekday, n)
    formatted_result = format_value_dt(result, month_date, weekday, n)
    log_file.write(formatted_result + "\n")
