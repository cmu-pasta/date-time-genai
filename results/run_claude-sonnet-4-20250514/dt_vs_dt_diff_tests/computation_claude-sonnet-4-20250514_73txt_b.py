
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, time
def is_within_business_hours(dt: datetime) -> bool:
    # Extract the time component from the datetime object
    current_time = dt.time()
    
    # Define business hours: 9 AM to 5 PM
    start_time = time(9, 0)   # 9:00 AM
    end_time = time(17, 0)    # 5:00 PM
    
    # Check if current time falls within business hours (inclusive)
    return start_time <= current_time <= end_time

# Entry point: is_within_business_hours(dt: datetime) -> bool

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_73txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_is_within_business_hours(dt):
    result = is_within_business_hours(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
