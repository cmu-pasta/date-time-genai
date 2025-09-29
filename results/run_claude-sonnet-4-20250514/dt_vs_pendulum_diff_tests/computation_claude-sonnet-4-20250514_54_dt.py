
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_year_percentage(dt: datetime) -> float:
    # Step 1: Get the year from the input date
    year = dt.year
    
    # Step 2: Calculate the day of the year (1-365 or 1-366)
    start_of_year = datetime(year, 1, 1)
    day_of_year = (dt - start_of_year).days + 1
    
    # Step 3: Determine if it's a leap year to get total days
    is_leap_year = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    total_days = 366 if is_leap_year else 365
    
    # Step 4: Calculate the percentage
    percentage = (day_of_year / total_days) * 100
    
    # Step 5: Return the result as a float
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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_54_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_year_percentage(dt):
    result = calculate_year_percentage(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
