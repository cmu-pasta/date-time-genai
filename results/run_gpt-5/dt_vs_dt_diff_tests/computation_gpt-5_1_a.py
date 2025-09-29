
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
def calculate_exact_time_difference(ts1: datetime, ts2: datetime) -> timedelta:
    """
    Calculate the exact time difference between two timezone-aware timestamps,
    correctly accounting for daylight saving time transitions.

    Parameters:
    - ts1: datetime with tzinfo=ZoneInfo
    - ts2: datetime with tzinfo=ZoneInfo

    Returns:
    - timedelta representing ts2 - ts1 (signed)
    """
    # Validate that both datetimes are timezone-aware and use ZoneInfo
    if ts1.tzinfo is None or ts2.tzinfo is None:
        raise ValueError("Both timestamps must be timezone-aware with ZoneInfo tzinfo.")
    if not isinstance(ts1.tzinfo, ZoneInfo) or not isinstance(ts2.tzinfo, ZoneInfo):
        raise ValueError("Both timestamps must have tzinfo set to ZoneInfo.")

    # Subtraction of aware datetimes uses their UTC offsets, honoring DST rules.
    return ts2 - ts1

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_1_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_exact_time_difference(ts1, ts2):
    result = calculate_exact_time_difference(ts1, ts2)
    formatted_result = format_value_dt(result, ts1, ts2)
    log_file.write(formatted_result + "\n")
