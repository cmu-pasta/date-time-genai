
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timezone
def calculate_age_in_seconds(birth_dt: datetime, reference_dt: datetime) -> int:
    # Validate input types
    if not isinstance(birth_dt, datetime) or not isinstance(reference_dt, datetime):
        raise TypeError("Both inputs must be datetime instances from the standard library.")

    # Determine timezone awareness
    def is_aware(dt: datetime) -> bool:
        return dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None

    birth_aware = is_aware(birth_dt)
    ref_aware = is_aware(reference_dt)

    # Ensure both datetimes are either naive or both aware
    if birth_aware != ref_aware:
        raise ValueError("Both datetimes must be either naive or timezone-aware.")

    # Normalize to UTC if timezone-aware to ensure correct chronological comparison
    if birth_aware:
        birth_norm = birth_dt.astimezone(timezone.utc)
        ref_norm = reference_dt.astimezone(timezone.utc)
    else:
        birth_norm = birth_dt
        ref_norm = reference_dt

    # Compute the difference
    delta = ref_norm - birth_norm

    # Age cannot be negative; clamp at zero seconds
    total_seconds = int(delta.total_seconds())
    return total_seconds if total_seconds >= 0 else 0

# Entry point: calculate_age_in_seconds(birth_dt: datetime, reference_dt: datetime) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_75txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_age_in_seconds(birth_dt, reference_dt):
    result = calculate_age_in_seconds(birth_dt, reference_dt)
    formatted_result = format_value_dt(result, birth_dt, reference_dt)
    log_file.write(formatted_result + "\n")
