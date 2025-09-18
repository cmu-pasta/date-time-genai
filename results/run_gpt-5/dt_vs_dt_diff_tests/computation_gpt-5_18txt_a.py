
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date, time, timedelta
def calculate_time_difference_hours(t1: time, t2: time) -> float:
    """
    Calculate the time difference in hours between two times.
    The result is the forward difference from t1 to t2 within a 24-hour cycle.
    """
    base_day = date(2000, 1, 1)
    dt1 = datetime.combine(base_day, t1)
    dt2 = datetime.combine(base_day, t2)
    delta = dt2 - dt1
    if delta < timedelta(0):
        # If t2 is earlier than t1, roll over to the next day
        delta += timedelta(days=1)
    return delta.total_seconds() / 3600.0

# Entry point: calculate_time_difference_hours(t1: time, t2: time) -> float

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_18txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy(), time_strategy())
def test_calculate_time_difference_hours(t1, t2):
    result = calculate_time_difference_hours(t1, t2)
    formatted_result = format_value_dt(result, t1, t2)
    log_file.write(formatted_result + "\n")
