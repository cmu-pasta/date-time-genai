
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
def exact_time_difference(ts1: datetime, ts2: datetime) -> timedelta:
    """
    Compute the exact time difference between two timestamps considering daylight saving time.
    Both inputs must be timezone-aware datetimes using ZoneInfo.
    Returns a signed timedelta: positive if ts2 is after ts1, negative otherwise.
    """
    # Validate that both datetimes are timezone-aware and use ZoneInfo
    if ts1.tzinfo is None or ts2.tzinfo is None:
        raise ValueError("Both timestamps must be timezone-aware (tzinfo set).")
    if not isinstance(ts1.tzinfo, ZoneInfo) or not isinstance(ts2.tzinfo, ZoneInfo):
        raise ValueError("Both timestamps must use zoneinfo.ZoneInfo for tzinfo.")

    # Normalize to UTC to account for DST transitions precisely
    ts1_utc = ts1.astimezone(ZoneInfo("UTC"))
    ts2_utc = ts2.astimezone(ZoneInfo("UTC"))

    # Compute and return the exact difference
    return ts2_utc - ts1_utc

# Entry point: exact_time_difference(ts1: datetime, ts2: datetime) -> timedelta

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_1_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_exact_time_difference(ts1, ts2):
    result = exact_time_difference(ts1, ts2)
    formatted_result = format_value_dt(result, ts1, ts2)
    log_file.write(formatted_result + "\n")
