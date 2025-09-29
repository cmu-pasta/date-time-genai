
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timezone
# Constants for lunar age calculation
_SYNODIC_MONTH_DAYS = 29.530588853  # Mean synodic month length in days
_REFERENCE_NEW_MOON = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)  # Known new moon epoch (UTC)

def calculate_lunar_age_days(dt: datetime) -> float:
    """
    Calculate the lunar age (days since the last new moon) for a given datetime.

    Assumptions:
    - If the input datetime is naive (no tzinfo), it is assumed to be in UTC.
    - The calculation uses a fixed mean synodic month length, so small deviations from
      true astronomical values may occur.

    Parameters:
    - dt: The datetime for which to compute lunar age.

    Returns:
    - A float representing the number of days since the last new moon (in [0, 29.530588853)).
    """
    # Ensure timezone-aware datetime in UTC
    if dt.tzinfo is None:
        dt_utc = dt.replace(tzinfo=timezone.utc)
    else:
        dt_utc = dt.astimezone(timezone.utc)

    # Compute difference in days from the reference new moon
    delta_seconds = (dt_utc - _REFERENCE_NEW_MOON).total_seconds()
    delta_days = delta_seconds / 86400.0

    # Lunar age is the positive remainder modulo the synodic month
    age = delta_days % _SYNODIC_MONTH_DAYS
    if age < 0.0:
        age += _SYNODIC_MONTH_DAYS

    return float(age)

# Entry point: calculate_lunar_age_days(dt: datetime) -> float

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_90txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_lunar_age_days(dt):
    result = calculate_lunar_age_days(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
