
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def find_next_friday_13th(given_date: datetime) -> datetime:
    # Start checking from the current month
    year = given_date.year
    month = given_date.month
    
    while True:
        # Create a date for the 13th of the current month
        thirteenth = datetime(year, month, 13)
        
        # Check if it's a Friday (weekday() returns 4 for Friday)
        if thirteenth.weekday() == 4:
            # Check if it's after the given date
            if thirteenth > given_date:
                return thirteenth
        
        # Move to the next month
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1

# Entry point: find_next_friday_13th(given_date: datetime) -> datetime

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_38_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_next_friday_13th(given_date):
    result = find_next_friday_13th(given_date)
    formatted_result = format_value_dt(result, given_date)
    log_file.write(formatted_result + "\n")
