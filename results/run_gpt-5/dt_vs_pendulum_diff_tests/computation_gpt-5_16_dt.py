
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timezone
def unix_to_datetime(timestamp: float, use_utc: bool) -> datetime:
    """
    Convert a Unix timestamp to a human-readable datetime.
    
    Args:
        timestamp: The Unix timestamp as a float or integer (seconds since the epoch).
        use_utc: If True, convert to a UTC-aware datetime; if False, convert to local time.
    
    Returns:
        A datetime object representing the human-readable time.
    """
    if use_utc:
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)
    else:
        return datetime.fromtimestamp(timestamp)

# Entry point: unix_to_datetime(timestamp: float, use_utc: bool) -> datetime

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_16_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(float_strategy(), bool_strategy())
def test_unix_to_datetime(timestamp, use_utc):
    result = unix_to_datetime(timestamp, use_utc)
    formatted_result = format_value_dt(result, timestamp, use_utc)
    log_file.write(formatted_result + "\n")
