
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta, timezone
import math
# Constants for lunar calculations
# Reference full moon (UTC): 2000-01-21 16:41:00 UTC (commonly used epoch)
_REF_FULL_MOON_UTC = datetime(2000, 1, 21, 16, 41, 0, tzinfo=timezone.utc)
# Mean synodic month length in days
_SYNODIC_MONTH = timedelta(days=29.530588853)

def next_full_moon(after: datetime) -> datetime:
    """
    Compute the datetime of the next full moon strictly after the given datetime.
    The result is returned as a timezone-aware UTC datetime.

    Note: This uses the mean synodic month and a fixed epoch for an approximate result.
    """
    # Normalize input to UTC (assume UTC if naive)
    if after.tzinfo is None:
        after_utc = after.replace(tzinfo=timezone.utc)
    else:
        after_utc = after.astimezone(timezone.utc)

    # Compute number of elapsed lunar cycles since the reference full moon
    cycles_elapsed = (after_utc - _REF_FULL_MOON_UTC) / _SYNODIC_MONTH

    # Find the index of the next full moon strictly after 'after'
    next_index = math.floor(cycles_elapsed) + 1

    # Compute the next full moon datetime in UTC
    next_full_moon_utc = _REF_FULL_MOON_UTC + next_index * _SYNODIC_MONTH
    return next_full_moon_utc

# Entry point: next_full_moon(after: datetime) -> datetime

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_23txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_next_full_moon(after):
    result = next_full_moon(after)
    formatted_result = format_value_dt(result, after)
    log_file.write(formatted_result + "\n")
