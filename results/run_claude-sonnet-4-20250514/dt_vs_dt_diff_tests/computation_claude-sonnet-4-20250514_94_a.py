
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def convert_to_modified_julian_date(dt: datetime) -> float:
    # Reference date for MJD 0: November 17, 1858 at midnight
    mjd_epoch = datetime(1858, 11, 17, 0, 0, 0)
    
    # Calculate the difference between input date and MJD epoch
    delta = dt - mjd_epoch
    
    # Convert to Modified Julian Date (including fractional days)
    # delta.days gives whole days, then add fractional part from time
    mjd = delta.days + (delta.seconds + delta.microseconds / 1000000.0) / 86400.0
    
    return mjd

# Entry point: convert_to_modified_julian_date(dt: datetime) -> float

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_dt_diff_test_logs", "log_computation_claude-sonnet-4-20250514_94_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_convert_to_modified_julian_date(dt):
    result = convert_to_modified_julian_date(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
