
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
from zoneinfo import ZoneInfo
def calculate_timezone_offset_hours(dt: datetime, tz: ZoneInfo) -> float:
    """
    Calculate the time zone offset in hours for a given datetime and timezone.

    Args:
        dt: A datetime object (naive or aware).
        tz: A ZoneInfo timezone.

    Returns:
        A float representing the UTC offset in hours for the given datetime in the specified timezone.
    """
    # Convert the datetime to the specified timezone to ensure accurate offset (handles DST)
    localized_dt = dt.astimezone(tz)

    # Obtain the UTC offset as a timedelta and convert to hours
    offset_td = localized_dt.utcoffset()
    offset_hours = offset_td.total_seconds() / 3600.0

    return float(offset_hours)

# Entry point: calculate_timezone_offset_hours(dt: datetime, tz: ZoneInfo) -> float

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_48_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), timezone_strategy())
def test_calculate_timezone_offset_hours(dt, tz):
    result = calculate_timezone_offset_hours(dt, tz)
    formatted_result = format_value_dt(result, dt, tz)
    log_file.write(formatted_result + "\n")
