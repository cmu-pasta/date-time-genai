
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
from zoneinfo import ZoneInfo
def convert_timezone(dt: datetime, source_timezone: ZoneInfo, target_timezone: ZoneInfo) -> datetime:
    """
    Converts a datetime object from one timezone to another.

    Args:
        dt: The datetime object to convert. If naive, it is assumed to be in the source_timezone.
            If timezone-aware, its existing timezone will be respected for the initial point in time.
        source_timezone: The ZoneInfo object for the initial timezone of the datetime.
                         This is used to localize 'dt' if it is naive.
        target_timezone: The ZoneInfo object for the desired target timezone.

    Returns:
        A datetime object representing the same point in time, but in the target_timezone.
    """
    # Step 1: Ensure the input datetime is timezone-aware and correctly interpreted
    # If dt is naive, localize it to the source_timezone.
    # If dt is already aware, astimezone() will correctly convert it,
    # or if we want to explicitly ensure it's treated as source_timezone initially
    # we can convert it to source_timezone first.
    # The most common interpretation for "convert from one timezone to another"
    # when input can be naive is to assume naive input IS in the source_timezone.
    if dt.tzinfo is None:
        # If naive, localize it to the source timezone.
        aware_dt_in_source = dt.replace(tzinfo=source_timezone)
    else:
        # If already aware, convert it to the source timezone first
        # to ensure it's based on the specified source_timezone before converting to target.
        # This handles cases where dt might be aware but in a different timezone than source_timezone.
        aware_dt_in_source = dt.astimezone(source_timezone)
    
    # Step 2: Convert the timezone-aware datetime to the target timezone
    converted_dt = aware_dt_in_source.astimezone(target_timezone)
    
    # Step 3: Return the result
    return converted_dt

# Entry point: convert_timezone(dt: datetime, source_timezone: ZoneInfo, target_timezone: ZoneInfo) -> datetime

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_dt_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_4_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), timezone_strategy(), timezone_strategy())
def test_convert_timezone(dt, source_timezone, target_timezone):
    result = convert_timezone(dt, source_timezone, target_timezone)
    formatted_result = format_value_dt(result, dt, source_timezone, target_timezone)
    log_file.write(formatted_result + "\n")
