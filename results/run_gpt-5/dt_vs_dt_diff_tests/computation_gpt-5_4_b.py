
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
from zoneinfo import ZoneInfo
def convert_timezone(dt: datetime, from_tz: ZoneInfo, to_tz: ZoneInfo) -> datetime:
    # Step 1: Ensure the datetime is associated with the source timezone
    if dt.tzinfo is None:
        aware_dt = dt.replace(tzinfo=from_tz)
    else:
        # Normalize the datetime to the source timezone in case it differs
        aware_dt = dt.astimezone(from_tz)
    # Step 2: Convert to the target timezone and return
    return aware_dt.astimezone(to_tz)

# Entry point: convert_timezone(dt: datetime, from_tz: ZoneInfo, to_tz: ZoneInfo) -> datetime

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_4_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), timezone_strategy(), timezone_strategy())
def test_convert_timezone(dt, from_tz, to_tz):
    result = convert_timezone(dt, from_tz, to_tz)
    formatted_result = format_value_dt(result, dt, from_tz, to_tz)
    log_file.write(formatted_result + "\n")
