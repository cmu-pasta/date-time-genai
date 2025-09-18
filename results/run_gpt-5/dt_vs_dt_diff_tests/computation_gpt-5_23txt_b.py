
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta, timezone, date
import math
# Constants for lunar phase calculations
_SYNODIC_MONTH = timedelta(days=29.530588853)  # Average synodic month length
_REF_FULL_MOON_UTC = datetime(2000, 1, 21, 4, 40, tzinfo=timezone.utc)  # Reference full moon (UTC)

def next_full_moon_after(dt: datetime) -> date:
    """
    Compute the calendar date of the next full moon strictly after the given datetime.
    
    Assumptions:
    - Uses an average synodic month; yields an approximation suitable for general use.
    - If 'dt' is naive, it is treated as UTC.
    
    Parameters:
    - dt: datetime -> The reference moment from which to find the next full moon.
    
    Returns:
    - date -> The calendar date (UTC) on which the next full moon occurs.
    """
    # Normalize input to UTC (treat naive datetimes as UTC)
    if dt.tzinfo is None:
        dt_utc = dt.replace(tzinfo=timezone.utc)
    else:
        dt_utc = dt.astimezone(timezone.utc)

    # Cycles elapsed since the reference full moon
    elapsed = dt_utc - _REF_FULL_MOON_UTC
    cycles = elapsed.total_seconds() / _SYNODIC_MONTH.total_seconds()

    # Next full moon index strictly after the input moment
    next_index = math.floor(cycles) + 1

    # Compute next full moon datetime in UTC
    next_full_moon_utc = _REF_FULL_MOON_UTC + _SYNODIC_MONTH * next_index

    # Return the calendar date (UTC)
    return next_full_moon_utc.date()

# Entry point: next_full_moon_after(dt: datetime) -> date

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_23txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_next_full_moon_after(dt):
    result = next_full_moon_after(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
