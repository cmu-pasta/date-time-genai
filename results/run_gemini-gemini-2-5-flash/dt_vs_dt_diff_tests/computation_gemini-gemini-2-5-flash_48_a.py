
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo # ZoneInfo is part of the datetime module since Python 3.9
def calculate_timezone_offset_in_hours(dt: datetime, tz: ZoneInfo) -> float:
    """
    Calculates the time zone offset in hours for a given datetime and timezone.

    Args:
        dt: The datetime object for which to calculate the offset. It can be naive or timezone-aware.
        tz: The ZoneInfo object representing the target timezone.

    Returns:
        The timezone offset in hours as a float.
    """
    # Step 1: Ensure the datetime object is correctly timezone-aware for the given ZoneInfo.
    # If dt is naive, we 'localize' it by assigning the tzinfo.
    # If dt is already aware, we convert it to the target timezone.
    if dt.tzinfo is None:
        # Interpret the naive datetime's components as being in the target timezone.
        dt_aware = dt.replace(tzinfo=tz)
    else:
        # Convert the existing timezone-aware datetime to the target timezone.
        dt_aware = dt.astimezone(tz)

    # Step 2: Get the UTC offset for this specific timezone-aware datetime.
    # utcoffset() returns a timedelta object.
    offset_timedelta: timedelta = dt_aware.utcoffset()

    # Step 3: Convert the timedelta offset to hours (float).
    if offset_timedelta is None:
        # This case should ideally not happen if dt_aware is properly constructed,
        # but as a safeguard, return 0.0 or raise an error if an offset cannot be determined.
        # For this problem, we'll assume a valid offset is always determinable.
        return 0.0 
        
    offset_hours: float = offset_timedelta.total_seconds() / 3600.0
    
    # Step 4: Return the result.
    return offset_hours

# Entry point: calculate_timezone_offset_in_hours(dt: datetime, tz: ZoneInfo) -> float

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_48_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), timezone_strategy())
def test_calculate_timezone_offset_in_hours(dt, tz):
    result = calculate_timezone_offset_in_hours(dt, tz)
    formatted_result = format_value_dt(result, dt, tz)
    log_file.write(formatted_result + "\n")
