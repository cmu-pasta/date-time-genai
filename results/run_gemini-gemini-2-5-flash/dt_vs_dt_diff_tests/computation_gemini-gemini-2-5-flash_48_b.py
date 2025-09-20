
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo # For Python 3.9+
def calculate_timezone_offset_in_hours(dt: datetime, target_timezone: ZoneInfo) -> float:
    # Step 1: Ensure the input datetime is associated with the target timezone.
    # We want the offset of 'target_timezone' at the time represented by 'dt'.
    # If dt is naive, we make it aware of the target_timezone.
    # If dt is already aware, we convert it to the target_timezone to get its specific offset.
    
    # First, if dt is naive, we replace its tzinfo directly.
    # If dt is aware, we convert it to the target_timezone.
    if dt.tzinfo is None:
        localized_dt = dt.replace(tzinfo=target_timezone)
    else:
        # If the input dt is already timezone-aware, convert it to the target_timezone
        # to ensure we get the offset for *that* specific timezone at that specific moment.
        localized_dt = dt.astimezone(target_timezone)

    # Step 2: Calculate the UTC offset for this localized datetime.
    # The utcoffset() method returns a timedelta object.
    offset_timedelta = localized_dt.utcoffset()

    # Step 3: Convert the timedelta offset to total hours as a float.
    # A timedelta is represented in seconds internally.
    if offset_timedelta is None:
        # This case should ideally not happen if localized_dt is properly timezone-aware.
        # However, for robustness, if for some reason utcoffset returns None, we return 0.0.
        return 0.0
    
    # Convert timedelta to total seconds and then divide by seconds in an hour.
    offset_in_hours = offset_timedelta.total_seconds() / 3600.0
    
    # Step 4: Return the result as a float.
    return offset_in_hours

# Entry point: calculate_timezone_offset_in_hours(dt: datetime, target_timezone: ZoneInfo) -> float

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_48_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), timezone_strategy())
def test_calculate_timezone_offset_in_hours(dt, target_timezone):
    result = calculate_timezone_offset_in_hours(dt, target_timezone)
    formatted_result = format_value_dt(result, dt, target_timezone)
    log_file.write(formatted_result + "\n")
