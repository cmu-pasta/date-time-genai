
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def find_previous_friday(dt: datetime) -> datetime:
    # Get the weekday (Monday=0, Tuesday=1, ..., Sunday=6)
    current_weekday = dt.weekday()
    
    # Calculate how many days to go back to reach the previous Friday
    # Friday is weekday 4
    days_back = (current_weekday - 4) % 7
    
    # Special case: if today is Friday, we want the previous Friday (7 days back)
    if days_back == 0:
        days_back = 7
    
    # Calculate the previous Friday by subtracting the required days
    previous_friday = dt - timedelta(days=days_back)
    
    return previous_friday

# Entry point: find_previous_friday(dt: datetime) -> datetime

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_20_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_previous_friday(dt):
    result = find_previous_friday(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
