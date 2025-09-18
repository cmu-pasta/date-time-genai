
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date, time
def calculate_minutes_between(t1: time, t2: time) -> int:
    """
    Calculate the absolute number of minutes between two times on the same day.
    Accepts datetime.time objects (naive or timezone-aware with the same tzinfo).
    Returns an integer number of minutes.
    """
    # Validate timezone compatibility
    if (t1.tzinfo is None) != (t2.tzinfo is None):
        raise ValueError("Both times must be either naive or timezone-aware.")
    if t1.tzinfo is not None and t1.tzinfo != t2.tzinfo:
        raise ValueError("Timezone-aware times must have the same tzinfo.")

    # Use an arbitrary same date for both times since they are on the same day
    same_day = date(2000, 1, 1)
    dt1 = datetime.combine(same_day, t1)
    dt2 = datetime.combine(same_day, t2)

    # Compute absolute difference in minutes
    delta_seconds = abs((dt2 - dt1).total_seconds())
    minutes = int(delta_seconds // 60)

    return minutes

# Entry point: calculate_minutes_between(t1: time, t2: time) -> int

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_33txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy(), time_strategy())
def test_calculate_minutes_between(t1, t2):
    result = calculate_minutes_between(t1, t2)
    formatted_result = format_value_dt(result, t1, t2)
    log_file.write(formatted_result + "\n")
