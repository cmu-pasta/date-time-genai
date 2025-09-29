
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
def find_dst_start_date(year: int, timezone: ZoneInfo) -> datetime:
    # Start from January 1st of the given year
    current_date = datetime(year, 1, 1, tzinfo=timezone)
    
    # Get the initial DST status
    previous_dst = current_date.dst() != timedelta(0)
    
    # Iterate through each day of the year
    for day in range(1, 366):  # 366 to handle leap years
        try:
            current_date = datetime(year, 1, 1, tzinfo=timezone) + timedelta(days=day-1)
            current_dst = current_date.dst() != timedelta(0)
            
            # If DST status changed from False to True, we found the start of DST
            if not previous_dst and current_dst:
                return current_date
            
            previous_dst = current_dst
            
        except ValueError:
            # Handle case where date doesn't exist (e.g., Feb 29 in non-leap year)
            continue
    
    # If no DST transition found, return None as datetime (this shouldn't happen in normal cases)
    # But since we need to return a datetime, return Jan 1st if no DST found
    return datetime(year, 1, 1, tzinfo=timezone)

# Entry point: find_dst_start_date(year: int, timezone: ZoneInfo) -> datetime

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_62_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timezone_strategy())
def test_find_dst_start_date(year, timezone):
    result = find_dst_start_date(year, timezone)
    formatted_result = format_value_dt(result, year, timezone)
    log_file.write(formatted_result + "\n")
