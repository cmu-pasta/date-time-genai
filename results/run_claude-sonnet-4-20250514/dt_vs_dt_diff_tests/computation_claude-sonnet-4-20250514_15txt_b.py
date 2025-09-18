
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def calculate_weekends_between_dates(start_date: datetime, end_date: datetime) -> int:
    # Ensure start_date is before end_date
    if start_date > end_date:
        start_date, end_date = end_date, start_date
    
    # Convert to date objects for easier comparison (ignore time component)
    current_date = start_date.date()
    end_date_only = end_date.date()
    
    weekend_count = 0
    
    # Iterate through each date in the range
    while current_date <= end_date_only:
        # Check if current date is Saturday (weekday() == 5)
        if current_date.weekday() == 5:
            # Check if the next day (Sunday) is still within our range
            next_day = current_date + timedelta(days=1)
            if next_day <= end_date_only:
                weekend_count += 1
        
        # Move to the next day
        current_date += timedelta(days=1)
    
    return weekend_count

# Entry point: calculate_weekends_between_dates(start_date: datetime, end_date: datetime) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_15txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_weekends_between_dates(start_date, end_date):
    result = calculate_weekends_between_dates(start_date, end_date)
    formatted_result = format_value_dt(result, start_date, end_date)
    log_file.write(formatted_result + "\n")
