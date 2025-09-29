
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_previous_friday(given_date: datetime) -> datetime:
    # Step 1: Get the day of the week (0=Monday, 1=Tuesday, ..., 4=Friday, 5=Saturday, 6=Sunday)
    current_weekday = given_date.weekday()
    
    # Step 2: Calculate how many days to go back to reach the previous Friday
    if current_weekday == 4:  # If it's already Friday
        days_back = 7  # Go back to previous Friday
    else:
        # Calculate days back: (current_weekday - 4) % 7
        # This gives us the correct number of days to subtract
        days_back = (current_weekday + 3) % 7
        if days_back == 0:
            days_back = 7
    
    # Actually, let's use a simpler approach:
    # Days back from current weekday to Friday (4)
    if current_weekday >= 4:  # Friday, Saturday, Sunday
        if current_weekday == 4:  # Friday
            days_back = 7
        else:  # Saturday or Sunday
            days_back = current_weekday - 4
    else:  # Monday, Tuesday, Wednesday, Thursday
        days_back = current_weekday + 3
    
    # Step 3: Subtract the calculated days using timedelta
    previous_friday = given_date - timedelta(days=days_back)
    
    return previous_friday

# Entry point: find_previous_friday(given_date: datetime) -> datetime

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_20_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_previous_friday(given_date):
    result = find_previous_friday(given_date)
    formatted_result = format_value_dt(result, given_date)
    log_file.write(formatted_result + "\n")
