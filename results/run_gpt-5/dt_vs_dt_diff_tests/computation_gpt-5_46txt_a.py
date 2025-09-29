
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, time
def to_12h_with_ampm(dt: datetime) -> time:
    """
    Convert a datetime (24-hour) to a 12-hour time with AM/PM encoded in time.fold.
    - Returns a time object with hour in 1..12.
    - AM/PM is indicated via fold: 0 = AM, 1 = PM.
    - tzinfo, minute, second, microsecond are preserved from the input datetime.
    """
    if not isinstance(dt, datetime):
        raise TypeError("Input must be a datetime instance")

    # Determine if PM
    is_pm = dt.hour >= 12

    # Convert to 12-hour clock: 0->12, 13->1, ..., 23->11, 12->12
    hour_12 = ((dt.hour + 11) % 12) + 1

    # Build time with fold indicating AM(0)/PM(1)
    t12 = time(
        hour=hour_12,
        minute=dt.minute,
        second=dt.second,
        microsecond=dt.microsecond,
        tzinfo=dt.tzinfo,
        fold=1 if is_pm else 0
    )
    return t12

# Entry point: to_12h_with_ampm(dt: datetime) -> time

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_46txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_to_12h_with_ampm(dt):
    result = to_12h_with_ampm(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
