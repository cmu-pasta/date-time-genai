
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta
def time_until_midnight(dt: datetime) -> timedelta:
    # Step 1: Determine if the datetime object is timezone-aware
    tzinfo = dt.tzinfo
    # Step 2: Construct the next day's midnight datetime (preserving the timezone, if any)
    next_midnight = datetime(dt.year, dt.month, dt.day, 0, 0, 0, 0, tzinfo=tzinfo) + timedelta(days=1)
    # Step 3: Calculate the difference between next midnight and the input datetime
    remaining = next_midnight - dt
    # Step 4: Return the result as a timedelta object
    return remaining

# Entry point: time_until_midnight(dt: datetime) -> timedelta

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_67txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_time_until_midnight(dt):
    result = time_until_midnight(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
