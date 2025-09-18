
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta, timezone
import math
# Constants for mean new moon calculations
# Reference: A known new moon occurred on 2000-01-06 18:14:00 UTC
EPOCH_NEW_MOON_UTC = datetime(2000, 1, 6, 18, 14, 0, tzinfo=timezone.utc)
SYNODIC_MONTH_DAYS = 29.530588853  # Mean synodic month

def next_new_moon(after: datetime) -> datetime:
    """
    Compute the datetime (UTC) of the next new moon strictly after the given datetime.

    If 'after' is timezone-naive, it is assumed to be in UTC.

    Parameters:
    - after: datetime

    Returns:
    - datetime (UTC): the moment of the next new moon after 'after'
    """
    # Normalize to UTC and ensure tz-aware
    if after.tzinfo is None:
        t = after.replace(tzinfo=timezone.utc)
    else:
        t = after.astimezone(timezone.utc)

    # Compute elapsed days since epoch
    elapsed_days = (t - EPOCH_NEW_MOON_UTC).total_seconds() / 86400.0

    # Determine the next lunation index strictly after 't'
    k = math.floor(elapsed_days / SYNODIC_MONTH_DAYS) + 1

    # Compute the candidate new moon time
    nm_time = EPOCH_NEW_MOON_UTC + timedelta(days=SYNODIC_MONTH_DAYS * k)

    # Guard against floating point round-off: ensure strictly after 't'
    if nm_time <= t:
        k += 1
        nm_time = EPOCH_NEW_MOON_UTC + timedelta(days=SYNODIC_MONTH_DAYS * k)

    return nm_time

# Entry point: next_new_moon(after: datetime) -> datetime

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_74txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_next_new_moon(after):
    result = next_new_moon(after)
    formatted_result = format_value_dt(result, after)
    log_file.write(formatted_result + "\n")
