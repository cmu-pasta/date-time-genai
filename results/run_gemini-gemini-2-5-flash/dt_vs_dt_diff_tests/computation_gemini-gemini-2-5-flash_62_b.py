
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
def find_dst_start_date(year: int, tz: ZoneInfo) -> datetime:
    """
    Finds the date when daylight saving time starts for a given year and timezone.
    This function searches from March 1st to April 30th to find the transition.
    
    Args:
        year: The year for which to find the DST start date.
        tz: The ZoneInfo object representing the timezone.
        
    Returns:
        A datetime object representing the start date of DST at midnight local time.
        Raises ValueError if DST start is not found within the typical search range.
    """
    
    # DST typically starts in March or April in the Northern Hemisphere.
    # We'll check from March 1st until end of April.
    
    # Start checking from March 1st
    current_date = datetime(year, 3, 1, 0, 0, 0)
    
    # Previous day's DST status, initialized to assume standard time before March 1st
    # This also handles cases where DST doesn't apply to the timezone or year.
    previous_dst_status = timedelta(0) 

    # Loop through days up to April 30th
    while current_date.month <= 4: # Check up to the end of April
        # Localize the current datetime (e.g., 1 AM local time to check DST status)
        # We choose 1 AM because the transition usually happens at 2 AM or 3 AM,
        # so 1 AM on the day of transition would still be standard time (or previous DST state).
        # We then check 1 AM on the *next* day to see if DST has applied.
        dt_at_1am_local = datetime(current_date.year, current_date.month, current_date.day, 1, 0, 0, tzinfo=tz)
        
        # Get the DST status for this specific localized datetime
        current_dst_status = dt_at_1am_local.dst()

        # Check for a transition from no DST to DST
        # If previous_dst_status was 0 (standard time) and current_dst_status is > 0 (DST is active)
        # This means the transition happened *between* the previous day's 1 AM and current day's 1 AM.
        if previous_dst_status == timedelta(0) and current_dst_status > timedelta(0):
            # The DST transition happened on 'current_date'.
            # We return a datetime object representing midnight of that date.
            return datetime(current_date.year, current_date.month, current_date.day, 0, 0, 0, tzinfo=tz)
        
        # Update previous status for the next iteration
        previous_dst_status = current_dst_status
        
        # Move to the next day
        current_date += timedelta(days=1)
        
    # If we reach here, DST start was not found within the search range
    raise ValueError(f"DST start not found for year {year} in timezone {tz.key} within March-April range.")

# Entry point: find_dst_start_date(year: int, tz: ZoneInfo) -> datetime

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_62_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timezone_strategy())
def test_find_dst_start_date(year, tz):
    result = find_dst_start_date(year, tz)
    formatted_result = format_value_dt(result, year, tz)
    log_file.write(formatted_result + "\n")
