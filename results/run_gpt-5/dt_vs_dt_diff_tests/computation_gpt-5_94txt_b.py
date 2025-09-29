
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timezone
from math import floor
def convert_to_mjd(dt: datetime) -> float:
    """
    Convert a datetime to Modified Julian Date (MJD).
    - If dt is timezone-aware, it is converted to UTC.
    - If dt is naive, it is assumed to be in UTC.
    Returns a float representing the MJD.
    """
    # Normalize to UTC
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
    # If naive, treat as UTC (no change needed)

    Y = dt.year
    M = dt.month
    D = dt.day

    # Time to fractional day
    day_fraction = (
        (dt.hour +
         dt.minute / 60.0 +
         (dt.second + dt.microsecond / 1_000_000.0) / 3600.0) / 24.0
    )

    # Algorithm for Julian Date (proleptic Gregorian calendar)
    if M <= 2:
        Yp = Y - 1
        Mp = M + 12
    else:
        Yp = Y
        Mp = M

    A = floor(Yp / 100)
    B = 2 - A + floor(A / 4)

    JD = (
        floor(365.25 * (Yp + 4716))
        + floor(30.6001 * (Mp + 1))
        + D
        + B
        - 1524.5
        + day_fraction
    )

    # Modified Julian Date
    MJD = JD - 2400000.5
    return MJD

# Entry point: convert_to_mjd(dt: datetime) -> float

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_94txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_convert_to_mjd(dt):
    result = convert_to_mjd(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
