
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
from zoneinfo import ZoneInfo
def calculate_timezone_offset(dt: datetime, tz: ZoneInfo) -> float:
    # Step 1: Localize the datetime to the given timezone
    localized_dt = dt.replace(tzinfo=tz)
    
    # Step 2: Get the UTC offset as a timedelta
    offset_delta = localized_dt.utcoffset()
    
    # Step 3: Convert timedelta to hours
    offset_hours = offset_delta.total_seconds() / 3600
    
    # Step 4: Return the offset in hours
    return offset_hours

# Entry point: calculate_timezone_offset(dt: datetime, tz: ZoneInfo) -> float

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_48_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), timezone_strategy())
def test_calculate_timezone_offset(dt, tz):
    result = calculate_timezone_offset(dt, tz)
    formatted_result = format_value_dt(result, dt, tz)
    log_file.write(formatted_result + "\n")
