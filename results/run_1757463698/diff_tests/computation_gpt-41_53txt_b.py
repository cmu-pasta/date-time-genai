
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def round_datetime_down(dt: datetime, minutes_interval: int) -> datetime:
    """
    Rounds down a datetime object to the nearest specified minute interval.
    
    Args:
        dt (datetime): The original datetime object.
        minutes_interval (int): The minute interval to round down to (e.g., 5 for every 5 minutes).
        
    Returns:
        datetime: The rounded down datetime object.
    """
    if minutes_interval <= 0 or minutes_interval > 60:
        raise ValueError("Interval must be between 1 and 60 minutes inclusive.")
    # Calculate the new minute component
    rounded_minute = (dt.minute // minutes_interval) * minutes_interval
    # Construct new datetime with rounded down values, set seconds and microseconds to 0
    return dt.replace(minute=rounded_minute, second=0, microsecond=0)

# Entry point: round_datetime_down(dt: datetime, minutes_interval: int) -> datetime

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_53txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), timestamp_strategy())
def test_round_datetime_down(dt, minutes_interval):
    result = round_datetime_down(dt, minutes_interval)
    formatted_result = format_value_dt(result, dt, minutes_interval)
    log_file.write(formatted_result + "\n")
