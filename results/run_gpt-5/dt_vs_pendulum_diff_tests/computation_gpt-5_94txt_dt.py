
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timezone
def datetime_to_mjd(dt: datetime) -> float:
    """
    Convert a datetime to Modified Julian Date (MJD).
    
    Assumptions:
    - If `dt` is naive (no tzinfo), it is interpreted as UTC.
    - Leap seconds are ignored (standard civil time handling).
    
    Returns:
    - MJD as a float.
    """
    # Step 1: Normalize to UTC (assume naive datetimes are UTC)
    if dt.tzinfo is None:
        dt_utc = dt.replace(tzinfo=timezone.utc)
    else:
        dt_utc = dt.astimezone(timezone.utc)

    # Step 2: Compute seconds since Unix epoch (1970-01-01T00:00:00Z)
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    seconds_since_epoch = (dt_utc - epoch).total_seconds()

    # Step 3: Convert seconds to days and add MJD at Unix epoch (40587.0)
    mjd = seconds_since_epoch / 86400.0 + 40587.0
    return mjd

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

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_94txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_datetime_to_mjd(dt):
    result = datetime_to_mjd(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
