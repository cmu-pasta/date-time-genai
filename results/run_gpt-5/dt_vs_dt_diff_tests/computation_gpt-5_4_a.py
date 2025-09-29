
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
from zoneinfo import ZoneInfo
def convert_timezone(ts: datetime, source_tz: ZoneInfo, target_tz: ZoneInfo) -> datetime:
    # Ensure the datetime is associated with the source timezone
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=source_tz)
    else:
        ts = ts.astimezone(source_tz)
    # Convert to the target timezone
    return ts.astimezone(target_tz)

# Entry point: convert_timezone(ts: datetime, source_tz: ZoneInfo, target_tz: ZoneInfo) -> datetime

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_4_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), timezone_strategy(), timezone_strategy())
def test_convert_timezone(ts, source_tz, target_tz):
    result = convert_timezone(ts, source_tz, target_tz)
    formatted_result = format_value_dt(result, ts, source_tz, target_tz)
    log_file.write(formatted_result + "\n")
