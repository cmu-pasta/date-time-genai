
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timezone, timedelta
def time_since_epoch(ts: datetime) -> timedelta:
    """
    Calculate the time elapsed since the Unix epoch for a given timestamp.

    - If 'ts' is timezone-aware, it is converted to UTC before computation.
    - If 'ts' is naive, it is compared against a naive epoch (1970-01-01 00:00:00).
    """
    # Case 1: Aware datetime -> compute against UTC epoch
    if ts.tzinfo is not None and ts.tzinfo.utcoffset(ts) is not None:
        epoch_utc = datetime(1970, 1, 1, tzinfo=timezone.utc)
        ts_utc = ts.astimezone(timezone.utc)
        return ts_utc - epoch_utc

    # Case 2: Naive datetime -> compute against naive epoch
    epoch_naive = datetime(1970, 1, 1)
    return ts - epoch_naive

# Entry point: time_since_epoch(ts: datetime) -> timedelta

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_30_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_time_since_epoch(ts):
    result = time_since_epoch(ts)
    formatted_result = format_value_dt(result, ts)
    log_file.write(formatted_result + "\n")
