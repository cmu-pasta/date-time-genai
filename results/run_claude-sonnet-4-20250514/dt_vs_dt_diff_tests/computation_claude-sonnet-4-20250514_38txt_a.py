
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def find_next_friday_13th(start_date: datetime) -> datetime:
    # Start from the current month and year
    year = start_date.year
    month = start_date.month
    
    while True:
        # Create a date for the 13th of the current month
        thirteenth = datetime(year, month, 13)
        
        # Check if this 13th is after our start date and is a Friday (weekday 4)
        if thirteenth > start_date and thirteenth.weekday() == 4:
            return thirteenth
        
        # Move to next month
        month += 1
        if month > 12:
            month = 1
            year += 1

# Entry point: find_next_friday_13th(start_date: datetime) -> datetime

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_38txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_next_friday_13th(start_date):
    result = find_next_friday_13th(start_date)
    formatted_result = format_value_dt(result, start_date)
    log_file.write(formatted_result + "\n")
