
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
from zoneinfo import ZoneInfo
def calculate_timezone_offset_hours(dt: datetime, timezone: ZoneInfo) -> float:
    # Step 1: Handle timezone-aware or naive datetime
    if dt.tzinfo is None:
        # Naive datetime - localize to the given timezone
        localized_dt = dt.replace(tzinfo=timezone)
    else:
        # Already timezone-aware - convert to the target timezone
        localized_dt = dt.astimezone(timezone)
    
    # Step 2: Get the UTC offset as a timedelta
    offset_timedelta = localized_dt.utcoffset()
    
    # Step 3: Convert timedelta to hours
    if offset_timedelta is not None:
        offset_hours = offset_timedelta.total_seconds() / 3600.0
    else:
        offset_hours = 0.0
    
    # Step 4: Return the offset in hours
    return offset_hours

# Entry point: calculate_timezone_offset_hours(dt: datetime, timezone: ZoneInfo) -> float

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_48_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), timezone_strategy())
def test_calculate_timezone_offset_hours(dt, timezone):
    result = calculate_timezone_offset_hours(dt, timezone)
    formatted_result = format_value_dt(result, dt, timezone)
    log_file.write(formatted_result + "\n")
