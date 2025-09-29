
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
from zoneinfo import ZoneInfo
def find_dst_end_date(year: int, timezone: ZoneInfo) -> datetime:
    # DST typically ends in fall, so we check October and November
    # Start from October 1st and check each day
    for month in [10, 11]:  # October and November
        for day in range(1, 32):  # Check all possible days in the month
            try:
                # Create datetime object for current date at 1 AM
                current_date = datetime(year, month, day, 1, 0, 0, tzinfo=timezone)
                # Create datetime object for next day at 1 AM
                next_date = datetime(year, month, day + 1, 1, 0, 0, tzinfo=timezone)
                
                # Check if DST status changes between current and next day
                current_dst = current_date.dst()
                next_dst = next_date.dst()
                
                # If current day has DST and next day doesn't, DST ends on next day
                if current_dst and not next_dst:
                    return next_date.replace(hour=0, minute=0, second=0, microsecond=0)
                    
            except ValueError:
                # Handle invalid dates (like Feb 30th)
                continue
    
    # If no DST transition found, return None as datetime (this shouldn't happen for DST zones)
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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_83_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timezone_strategy())
def test_find_dst_end_date(year, timezone):
    result = find_dst_end_date(year, timezone)
    formatted_result = format_value_dt(result, year, timezone)
    log_file.write(formatted_result + "\n")
