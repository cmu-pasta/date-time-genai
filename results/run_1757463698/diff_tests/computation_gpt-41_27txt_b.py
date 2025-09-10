
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def midpoint_between_datetimes(dt1: datetime, dt2: datetime) -> datetime:
    # Step 1: Calculate the difference
    difference = dt2 - dt1

    # Step 2: Compute half of the difference (midpoint duration)
    half_difference = difference / 2

    # Step 3: Find the earlier datetime as the base
    if dt1 < dt2:
        midpoint = dt1 + half_difference
    else:
        midpoint = dt2 + (-half_difference)

    # Step 4: Return the midpoint datetime
    return midpoint

# Entry point: midpoint_between_datetimes(dt1: datetime, dt2: datetime) -> datetime

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

if not os.path.exists(".logs/diff_test_logs"):
    os.makedirs(".logs/diff_test_logs")
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_27txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_midpoint_between_datetimes(dt1, dt2):
    result = midpoint_between_datetimes(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
