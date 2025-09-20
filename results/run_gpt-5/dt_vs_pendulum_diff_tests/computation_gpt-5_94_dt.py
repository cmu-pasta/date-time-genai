
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timezone
def datetime_to_mjd(dt: datetime) -> float:
    """
    Convert a datetime to Modified Julian Date (MJD).
    - If dt is timezone-aware, it is converted to UTC.
    - If dt is naive, it is assumed to be in UTC.
    Returns a float MJD.
    """
    # Step 1: Normalize to UTC
    if dt.tzinfo is None:
        dt_utc = dt.replace(tzinfo=timezone.utc)
    else:
        dt_utc = dt.astimezone(timezone.utc)

    # Step 2: Compute seconds since Unix epoch in UTC using datetime arithmetic
    unix_epoch_utc = datetime(1970, 1, 1, tzinfo=timezone.utc)
    seconds_since_epoch = (dt_utc - unix_epoch_utc).total_seconds()

    # Step 3: Convert to Modified Julian Date
    # MJD = 40587.0 + (seconds since epoch)/86400
    mjd = 40587.0 + (seconds_since_epoch / 86400.0)

    # Step 4: Return the result as a float
    return float(mjd)

# Entry point: datetime_to_mjd(dt: datetime) -> float

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_94_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_datetime_to_mjd(dt):
    result = datetime_to_mjd(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
