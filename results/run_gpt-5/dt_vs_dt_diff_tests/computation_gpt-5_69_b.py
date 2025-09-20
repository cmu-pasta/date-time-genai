
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
def calculate_timezone_difference(dt1: datetime, tz1: ZoneInfo, dt2: datetime, tz2: ZoneInfo) -> timedelta:
    """
    Calculate the time difference between two datetimes, each associated with its own time zone.
    The result accounts for time zone offsets and daylight saving transitions.

    Args:
        dt1: The first datetime (naive or aware).
        tz1: The time zone for the first datetime.
        dt2: The second datetime (naive or aware).
        tz2: The time zone for the second datetime.

    Returns:
        A timedelta representing dt2 - dt1 as an instant difference, accounting for time zones.
    """
    # Normalize dt1 to be aware in tz1
    if dt1.tzinfo is None:
        dt1_aware = dt1.replace(tzinfo=tz1)
    else:
        dt1_aware = dt1.astimezone(tz1)

    # Normalize dt2 to be aware in tz2
    if dt2.tzinfo is None:
        dt2_aware = dt2.replace(tzinfo=tz2)
    else:
        dt2_aware = dt2.astimezone(tz2)

    # Compute the difference as an instant difference (accounts for time zones)
    return dt2_aware - dt1_aware

# Entry point: calculate_timezone_difference(dt1: datetime, tz1: ZoneInfo, dt2: datetime, tz2: ZoneInfo) -> timedelta

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_69_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), timezone_strategy(), datetime_strategy(), timezone_strategy())
def test_calculate_timezone_difference(dt1, tz1, dt2, tz2):
    result = calculate_timezone_difference(dt1, tz1, dt2, tz2)
    formatted_result = format_value_dt(result, dt1, tz1, dt2, tz2)
    log_file.write(formatted_result + "\n")
