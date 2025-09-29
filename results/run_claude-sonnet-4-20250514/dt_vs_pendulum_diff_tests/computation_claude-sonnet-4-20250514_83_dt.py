
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
from zoneinfo import ZoneInfo
def find_dst_end_date(year: int, timezone: ZoneInfo) -> datetime:
    # Start checking from October 1st as DST typically ends in fall
    # Iterate through each day to find when the UTC offset changes
    for month in [10, 11, 12]:  # Check October, November, December
        for day in range(1, 32):
            try:
                # Create a datetime at 1 AM for the current date
                current_date = datetime(year, month, day, 1, tzinfo=timezone)
                
                # Create a datetime for the next day at 1 AM
                if day == 31:
                    if month == 12:
                        continue  # Skip if we're at the end of year
                    next_date = datetime(year, month + 1, 1, 1, tzinfo=timezone)
                else:
                    next_date = datetime(year, month, day + 1, 1, tzinfo=timezone)
                
                # Get UTC offsets for both dates
                current_offset = current_date.utcoffset()
                next_offset = next_date.utcoffset()
                
                # If the offset increases (less negative), DST has ended
                if next_offset > current_offset:
                    return next_date.replace(hour=2, minute=0, second=0, microsecond=0)
                    
            except ValueError:
                # Skip invalid dates (like February 30th)
                continue
    
    # If no transition found, return None converted to a datetime
    # This handles timezones that don't observe DST
    return datetime(year, 1, 1, tzinfo=timezone)

# Entry point: find_dst_end_date(year: int, timezone: ZoneInfo) -> datetime

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_83_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timezone_strategy())
def test_find_dst_end_date(year, timezone):
    result = find_dst_end_date(year, timezone)
    formatted_result = format_value_dt(result, year, timezone)
    log_file.write(formatted_result + "\n")
