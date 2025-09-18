
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def datetime_to_mjd(dt: datetime) -> float:
    # MJD epoch: November 17, 1858 at midnight (00:00:00)
    mjd_epoch = datetime(1858, 11, 17, 0, 0, 0)
    
    # Calculate the difference between the input datetime and MJD epoch
    time_difference = dt - mjd_epoch
    
    # Convert the difference to days (including fractional parts)
    # total_seconds() gives us the total seconds in the timedelta
    # Divide by 86400 (seconds in a day) to get days
    mjd = time_difference.total_seconds() / 86400.0
    
    return mjd

# Entry point: datetime_to_mjd(dt: datetime) -> float

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_94txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_datetime_to_mjd(dt):
    result = datetime_to_mjd(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
