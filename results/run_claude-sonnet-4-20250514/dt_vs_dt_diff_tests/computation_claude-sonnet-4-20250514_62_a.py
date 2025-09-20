
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
from zoneinfo import ZoneInfo
def find_dst_start(year: int, timezone: ZoneInfo) -> datetime:
    # Start checking from January 1st of the given year
    current_date = datetime(year, 1, 1, tzinfo=timezone)
    
    # Get the initial UTC offset for the year
    previous_offset = current_date.utcoffset()
    
    # Check each day of the year for DST transition
    for day in range(1, 367):  # 366 days to handle leap years
        try:
            current_date = datetime(year, 1, 1, tzinfo=timezone).replace(day=1) + (datetime(year, 1, day, tzinfo=timezone) - datetime(year, 1, 1, tzinfo=timezone))
            current_date = datetime(year, 1, 1, tzinfo=timezone)
            
            # Calculate the current date by adding days
            days_to_add = day - 1
            month = 1
            day_of_month = 1 + days_to_add
            
            # Handle month/day calculation manually
            days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                days_in_months[1] = 29  # Leap year
            
            while day_of_month > days_in_months[month - 1]:
                day_of_month -= days_in_months[month - 1]
                month += 1
                if month > 12:
                    break
            
            if month > 12:
                break
                
            current_date = datetime(year, month, day_of_month, tzinfo=timezone)
            current_offset = current_date.utcoffset()
            
            # DST typically starts when offset becomes more negative (spring forward)
            if current_offset != previous_offset and current_offset < previous_offset:
                return current_date
                
            previous_offset = current_offset
            
        except ValueError:
            # Handle invalid dates (like Feb 30)
            continue
    
    # If no DST transition found, return January 1st (timezone doesn't observe DST)
    return datetime(year, 1, 1, tzinfo=timezone)

# Entry point: find_dst_start(year: int, timezone: ZoneInfo) -> datetime

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_62_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timezone_strategy())
def test_find_dst_start(year, timezone):
    result = find_dst_start(year, timezone)
    formatted_result = format_value_dt(result, year, timezone)
    log_file.write(formatted_result + "\n")
