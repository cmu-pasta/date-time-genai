
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def timestamp_to_rfc2822(dt: datetime) -> str:
    """
    Convert a datetime object to RFC 2822 format.
    Example output: 'Wed, 02 Oct 2002 13:00:00 -0400'
    """
    # Step 1: Check if tzinfo is present; if not, treat as local time with no offset
    if dt.tzinfo is None:
        offset_str = "-0000"
    else:
        # Get the UTC offset in seconds and compute hours and minutes
        offset = dt.utcoffset()
        if offset is None:
            offset_str = "-0000"
        else:
            total_minutes = int(offset.total_seconds() // 60)
            sign = "+" if total_minutes >= 0 else "-"
            total_minutes = abs(total_minutes)
            hours, minutes = divmod(total_minutes, 60)
            offset_str = f"{sign}{hours:02d}{minutes:02d}"

    # Step 2: Format datetime in RFC 2822 format
    # Example: 'Wed, 02 Oct 2002 13:00:00 -0400'
    rfc2822 = dt.strftime('%a, %d %b %Y %H:%M:%S ') + offset_str

    # Step 3: Return the formatted string
    return rfc2822

# Entry point: timestamp_to_rfc2822(dt: datetime) -> str

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_41txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_timestamp_to_rfc2822(dt):
    result = timestamp_to_rfc2822(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
