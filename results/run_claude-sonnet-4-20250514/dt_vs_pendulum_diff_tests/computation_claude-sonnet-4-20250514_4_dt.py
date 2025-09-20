
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
from zoneinfo import ZoneInfo
def convert_timezone(dt: datetime, target_timezone: ZoneInfo) -> datetime:
    # Step 1: Convert the datetime to the target timezone
    converted_dt = dt.astimezone(target_timezone)
    
    # Step 2: Return the converted datetime
    return converted_dt

# Entry point: convert_timezone(dt: datetime, target_timezone: ZoneInfo) -> datetime

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_4_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), timezone_strategy())
def test_convert_timezone(dt, target_timezone):
    result = convert_timezone(dt, target_timezone)
    formatted_result = format_value_dt(result, dt, target_timezone)
    log_file.write(formatted_result + "\n")
