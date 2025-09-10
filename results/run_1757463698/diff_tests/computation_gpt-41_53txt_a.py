
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def round_down_datetime(dt: datetime, interval_minutes: int) -> datetime:
    # Step 1: Calculate the number of minutes since midnight
    minutes_since_midnight = dt.hour * 60 + dt.minute
    # Step 2: Round down to nearest multiple of interval
    rounded_minutes = (minutes_since_midnight // interval_minutes) * interval_minutes
    # Step 3: Rebuild new datetime with rounded down time
    rounded_dt = dt.replace(hour=rounded_minutes // 60, minute=rounded_minutes % 60, second=0, microsecond=0)
    return rounded_dt

# Entry point: round_down_datetime(dt: datetime, interval_minutes: int) -> datetime

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_53txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), timestamp_strategy())
def test_round_down_datetime(dt, interval_minutes):
    result = round_down_datetime(dt, interval_minutes)
    formatted_result = format_value_dt(result, dt, interval_minutes)
    log_file.write(formatted_result + "\n")
