
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_year_percentage(dt: datetime) -> float:
    # Step 1: Get the year from the given date
    year = dt.year
    
    # Step 2: Create datetime for January 1st of that year
    start_of_year = datetime(year, 1, 1)
    
    # Step 3: Calculate days passed from start of year to given date
    days_passed = (dt - start_of_year).days
    
    # Step 4: Calculate total days in the year
    start_of_next_year = datetime(year + 1, 1, 1)
    total_days_in_year = (start_of_next_year - start_of_year).days
    
    # Step 5: Calculate percentage
    percentage = (days_passed / total_days_in_year) * 100
    
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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_54_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_year_percentage(dt):
    result = calculate_year_percentage(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
