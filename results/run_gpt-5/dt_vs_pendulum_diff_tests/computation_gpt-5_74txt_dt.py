
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta, timezone, date
import math
# Constants: average synodic month and a well-known reference new moon
_SYNODIC_MONTH_DAYS = 29.530588853  # mean synodic month length
_SYNODIC_MONTH = timedelta(days=_SYNODIC_MONTH_DAYS)

# Reference new moon: 2000-01-06 18:14 UTC (widely used epoch)
_REF_NEW_MOON_UTC = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)

def next_new_moon(after_dt: datetime) -> date:
    """
    Compute the UTC calendar date of the next new moon strictly after the given moment.
    - If 'after_dt' is naive, it is interpreted as UTC.
    - The returned value is the date in UTC on which the next new moon occurs.
    """
    # Normalize input to timezone-aware UTC
    if after_dt.tzinfo is None:
        dt_utc = after_dt.replace(tzinfo=timezone.utc)
    else:
        dt_utc = after_dt.astimezone(timezone.utc)

    # Compute how many synodic cycles have elapsed since the reference new moon
    elapsed = dt_utc - _REF_NEW_MOON_UTC
    cycles_elapsed = elapsed / _SYNODIC_MONTH  # float number of cycles

    # We want the next new moon strictly after the input time
    next_cycle_index = math.floor(cycles_elapsed) + 1

    # Compute the instant of the next new moon and return its UTC date
    next_new_moon_dt = _REF_NEW_MOON_UTC + next_cycle_index * _SYNODIC_MONTH
    return next_new_moon_dt.date()

# Entry point: next_new_moon(after_dt: datetime) -> date

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_74txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_next_new_moon(after_dt):
    result = next_new_moon(after_dt)
    formatted_result = format_value_dt(result, after_dt)
    log_file.write(formatted_result + "\n")
