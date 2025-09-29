
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
def calculate_exact_time_difference(ts1: datetime, ts2: datetime) -> timedelta:
    """
    Calculate the exact time difference between two timestamps considering daylight saving time (DST).

    Requirements:
    - ts1 and ts2 must be timezone-aware datetime objects (i.e., have tzinfo set).
    - If you need to specify a time zone, construct your datetimes with tzinfo=ZoneInfo("Region/City").
      The 'fold' attribute can be set on the datetime to disambiguate ambiguous times during DST fall-back.

    The function returns a signed timedelta: positive if ts2 occurs after ts1, negative otherwise.
    """
    if ts1.tzinfo is None or ts2.tzinfo is None:
        raise ValueError("Both timestamps must be timezone-aware to account for DST.")

    # Normalize both timestamps to UTC to ensure correct arithmetic across DST transitions
    ts1_utc = ts1.astimezone(timezone.utc)
    ts2_utc = ts2.astimezone(timezone.utc)

    # Compute signed difference
    return ts2_utc - ts1_utc

# Entry point: calculate_exact_time_difference(ts1: datetime, ts2: datetime) -> timedelta

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

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_1txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_exact_time_difference(ts1, ts2):
    result = calculate_exact_time_difference(ts1, ts2)
    formatted_result = format_value_dt(result, ts1, ts2)
    log_file.write(formatted_result + "\n")
