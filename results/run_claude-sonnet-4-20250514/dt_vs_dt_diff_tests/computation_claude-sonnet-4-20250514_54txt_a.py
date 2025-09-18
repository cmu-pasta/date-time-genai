
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_year_percentage(dt: datetime) -> float:
    # Get the start of the year (January 1st)
    start_of_year = datetime(dt.year, 1, 1)
    
    # Get the start of next year
    start_of_next_year = datetime(dt.year + 1, 1, 1)
    
    # Calculate total days in the year
    total_days = (start_of_next_year - start_of_year).days
    
    # Calculate days passed since start of year
    days_passed = (dt - start_of_year).days
    
    # Calculate percentage
    percentage = (days_passed / total_days) * 100
    
    return percentage

# Entry point: calculate_year_percentage(dt: datetime) -> float

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_54txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_year_percentage(dt):
    result = calculate_year_percentage(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
