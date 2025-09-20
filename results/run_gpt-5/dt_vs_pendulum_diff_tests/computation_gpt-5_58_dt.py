
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta, timezone
def convert_epoch(timestamp: float, from_epoch: datetime, to_epoch: datetime) -> float:
    # Ensure both epochs are treated in UTC for consistent calculations
    def _to_utc(dt: datetime) -> datetime:
        # Treat naive datetimes as UTC; convert aware datetimes to UTC
        return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)

    fe = _to_utc(from_epoch)
    te = _to_utc(to_epoch)

    # Compute the absolute instant represented by the timestamp relative to from_epoch
    instant = fe + timedelta(seconds=timestamp)

    # Convert the instant to seconds relative to to_epoch
    result = (instant - te).total_seconds()
    return result

# Example usage (Unix to Windows epoch seconds):
# unix_epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
# windows_epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
# windows_seconds = convert_epoch(0.0, unix_epoch, windows_epoch)  # 11644473600.0

# Entry point: convert_epoch(timestamp: float, from_epoch: datetime, to_epoch: datetime) -> float

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_58_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(float_strategy(), datetime_strategy(), datetime_strategy())
def test_convert_epoch(timestamp, from_epoch, to_epoch):
    result = convert_epoch(timestamp, from_epoch, to_epoch)
    formatted_result = format_value_dt(result, timestamp, from_epoch, to_epoch)
    log_file.write(formatted_result + "\n")
