
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def convert_to_12hour_format(dt: datetime) -> str:
    # Step 1: Extract the hour from the datetime object
    hour = dt.hour
    minute = dt.minute
    second = dt.second
    
    # Step 2: Determine AM/PM and convert hour to 12-hour format
    if hour == 0:
        # Midnight case: 0:xx -> 12:xx AM
        hour_12 = 12
        am_pm = "AM"
    elif hour < 12:
        # Morning hours: 1-11 -> 1-11 AM
        hour_12 = hour
        am_pm = "AM"
    elif hour == 12:
        # Noon case: 12:xx -> 12:xx PM
        hour_12 = 12
        am_pm = "PM"
    else:
        # Afternoon/Evening hours: 13-23 -> 1-11 PM
        hour_12 = hour - 12
        am_pm = "PM"
    
    # Step 3: Format the result as 12-hour format with AM/PM
    formatted_time = f"{hour_12}:{minute:02d}:{second:02d} {am_pm}"
    
    return formatted_time

# Entry point: convert_to_12hour_format(dt: datetime) -> str

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_46_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_convert_to_12hour_format(dt):
    result = convert_to_12hour_format(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
