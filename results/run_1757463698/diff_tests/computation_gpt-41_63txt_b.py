
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
import re
def parse_iso8601_duration(duration: str) -> timedelta:
    """
    Parse an ISO 8601 duration string (e.g., "P3DT4H5M6S") into a timedelta.
    Only supports days, hours, minutes, seconds (no months or years).
    """
    pattern = (
        r'P'                         # starts with 'P'
        r'(?:(\d+)D)?'               # days
        r'(?:T'                      # time part begins with 'T'
        r'(?:(\d+)H)?'               # hours
        r'(?:(\d+)M)?'               # minutes
        r'(?:(\d+)S)?'               # seconds
        r')?$'
    )
    match = re.fullmatch(pattern, duration)
    if not match:
        raise ValueError(f"Invalid ISO 8601 duration: {duration}")
    days = int(match.group(1)) if match.group(1) else 0
    hours = int(match.group(2)) if match.group(2) else 0
    minutes = int(match.group(3)) if match.group(3) else 0
    seconds = int(match.group(4)) if match.group(4) else 0
    return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

def add_or_subtract_iso8601_duration(dt: datetime, iso_duration: str, add: bool) -> datetime:
    """
    Add or subtract an ISO 8601 duration (string) to/from a datetime object.

    Args:
        dt (datetime): The original datetime.
        iso_duration (str): ISO 8601 duration string (e.g., 'P1DT3H').
        add (bool): True to add, False to subtract.

    Returns:
        datetime: The resulting datetime after addition or subtraction.
    """
    duration = parse_iso8601_duration(iso_duration)
    if add:
        result = dt + duration
    else:
        result = dt - duration
    return result

# Entry point: add_or_subtract_iso8601_duration(dt: datetime, iso_duration: str, add: bool) -> datetime

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

if not os.path.exists(".logs/diff_test_logs"):
    os.makedirs(".logs/diff_test_logs")
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_63txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), string_strategy(), bool_strategy())
def test_add_or_subtract_iso8601_duration(dt, iso_duration, add):
    result = add_or_subtract_iso8601_duration(dt, iso_duration, add)
    formatted_result = format_value_dt(result, dt, iso_duration, add)
    log_file.write(formatted_result + "\n")
