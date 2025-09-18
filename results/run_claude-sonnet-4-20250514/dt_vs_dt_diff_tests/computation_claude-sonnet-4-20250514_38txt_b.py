
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def find_next_friday_13th(start_date: date) -> date:
    # Start checking from the current month
    current_year = start_date.year
    current_month = start_date.month
    
    while True:
        # Create the 13th of the current month
        thirteenth = date(current_year, current_month, 13)
        
        # Check if it's a Friday (weekday() returns 4 for Friday) and after start_date
        if thirteenth.weekday() == 4 and thirteenth > start_date:
            return thirteenth
        
        # Move to next month
        current_month += 1
        if current_month > 12:
            current_month = 1
            current_year += 1

# Entry point: find_next_friday_13th(start_date: date) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_38txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_find_next_friday_13th(start_date):
    result = find_next_friday_13th(start_date)
    formatted_result = format_value_dt(result, start_date)
    log_file.write(formatted_result + "\n")
