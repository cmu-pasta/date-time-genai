
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timezone, timedelta
def _to_utc(dt: datetime) -> datetime:
    # Treat naive datetimes as UTC; convert aware datetimes to UTC
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)

def convert_timestamp_between_epochs(timestamp: float, source_epoch: datetime, target_epoch: datetime) -> float:
    # Normalize epochs to UTC to avoid timezone inconsistencies
    src_epoch_utc = _to_utc(source_epoch)
    tgt_epoch_utc = _to_utc(target_epoch)
    # Compute the absolute moment represented by the source timestamp
    instant = src_epoch_utc + timedelta(seconds=timestamp)
    # Return seconds relative to the target epoch
    return (instant - tgt_epoch_utc).total_seconds()

def convert_unix_to_windows_seconds(unix_seconds: float) -> float:
    # Unix epoch: 1970-01-01 UTC, Windows FILETIME epoch: 1601-01-01 UTC
    unix_epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    windows_epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
    return convert_timestamp_between_epochs(unix_seconds, unix_epoch, windows_epoch)

def convert_windows_to_unix_seconds(windows_seconds: float) -> float:
    windows_epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
    unix_epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    return convert_timestamp_between_epochs(windows_seconds, windows_epoch, unix_epoch)

# Entry point: convert_timestamp_between_epochs(timestamp: float, source_epoch: datetime, target_epoch: datetime) -> float

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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_58txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(float_strategy(), datetime_strategy(), datetime_strategy())
def test_convert_timestamp_between_epochs(timestamp, source_epoch, target_epoch):
    result = convert_timestamp_between_epochs(timestamp, source_epoch, target_epoch)
    formatted_result = format_value_dt(result, timestamp, source_epoch, target_epoch)
    log_file.write(formatted_result + "\n")
