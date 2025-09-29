
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timezone
# Constants
SYNODIC_MONTH_DAYS = 29.530588853  # Average synodic month length in days
# Reference new moon: 2000-01-06 18:14:00 UTC (commonly used epoch for lunar calculations)
NEW_MOON_EPOCH_UTC = datetime(2000, 1, 6, 18, 14, 0, tzinfo=timezone.utc)

def lunar_age_days_since_new_moon(dt: datetime) -> float:
    """
    Calculate the lunar age (days since the last new moon) for a given datetime.
    
    Rules and assumptions:
    - If dt is naive (no tzinfo), it is assumed to be in UTC.
    - If dt is timezone-aware, it is converted to UTC.
    - The result is a float representing days since the most recent new moon, in [0, SYNODIC_MONTH_DAYS).
    """
    # Normalize input datetime to UTC
    if dt.tzinfo is None:
        dt_utc = dt.replace(tzinfo=timezone.utc)
    else:
        dt_utc = dt.astimezone(timezone.utc)
    
    # Compute elapsed time in days since the reference new moon epoch
    elapsed_seconds = (dt_utc - NEW_MOON_EPOCH_UTC).total_seconds()
    elapsed_days = elapsed_seconds / 86400.0
    
    # Modulo to get days since the most recent new moon (ensure non-negative)
    age_days = elapsed_days % SYNODIC_MONTH_DAYS
    return float(age_days)

# Entry point: lunar_age_days_since_new_moon(dt: datetime) -> float

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_90txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_lunar_age_days_since_new_moon(dt):
    result = lunar_age_days_since_new_moon(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
