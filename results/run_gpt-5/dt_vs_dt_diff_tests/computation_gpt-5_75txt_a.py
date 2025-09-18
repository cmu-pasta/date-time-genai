
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_chronological_age_seconds(birth_dt: datetime, as_of: datetime) -> int:
    """
    Calculate the chronological age in seconds between a birth datetime and a reference datetime.

    Parameters:
    - birth_dt: datetime of birth (naive or timezone-aware).
    - as_of: reference datetime at which to compute age (must match awareness of birth_dt).

    Returns:
    - int: number of seconds between birth_dt and as_of. Can be negative if as_of < birth_dt.
    """
    if not isinstance(birth_dt, datetime) or not isinstance(as_of, datetime):
        raise TypeError("Both birth_dt and as_of must be datetime instances.")

    # Ensure both datetimes are either both naive or both timezone-aware
    if (birth_dt.tzinfo is None) != (as_of.tzinfo is None):
        raise ValueError("birth_dt and as_of must both be naive or both be timezone-aware.")

    delta = as_of - birth_dt
    return int(delta.total_seconds())

# Entry point: calculate_chronological_age_seconds(birth_dt: datetime, as_of: datetime) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_75txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_chronological_age_seconds(birth_dt, as_of):
    result = calculate_chronological_age_seconds(birth_dt, as_of)
    formatted_result = format_value_dt(result, birth_dt, as_of)
    log_file.write(formatted_result + "\n")
