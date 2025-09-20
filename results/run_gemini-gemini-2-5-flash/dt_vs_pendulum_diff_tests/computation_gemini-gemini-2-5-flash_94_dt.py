
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timedelta, timezone
def convert_to_modified_julian_date(dt_input: datetime) -> float:
    # Step 1: Define the Modified Julian Date epoch (November 17, 1858, 00:00:00 UTC)
    mjd_epoch = datetime(1858, 11, 17, 0, 0, 0, tzinfo=timezone.utc)
    
    # Step 2: Ensure the input datetime is in UTC for accurate calculation.
    # If the input datetime is naive, we assume it's UTC for MJD purposes.
    # If it's timezone-aware, convert it to UTC.
    if dt_input.tzinfo is None:
        dt_utc = dt_input.replace(tzinfo=timezone.utc)
    else:
        dt_utc = dt_input.astimezone(timezone.utc)
        
    # Step 3: Calculate the time difference (timedelta) from the MJD epoch to the input datetime.
    time_difference: timedelta = dt_utc - mjd_epoch
    
    # Step 4: Convert the timedelta to a total number of days (float).
    # A day has 86400 seconds.
    modified_julian_date: float = time_difference.total_seconds() / (24 * 60 * 60)
    
    # Step 5: Return the Modified Julian Date as a float.
    return modified_julian_date

# Entry point: convert_to_modified_julian_date(dt_input: datetime) -> float

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_94_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_convert_to_modified_julian_date(dt_input):
    result = convert_to_modified_julian_date(dt_input)
    formatted_result = format_value_dt(result, dt_input)
    log_file.write(formatted_result + "\n")
