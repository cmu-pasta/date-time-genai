
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def get_iso8601_string(dt: datetime) -> str:
    # Step 1: Use the isoformat() method to get the ISO 8601 formatted string
    iso_string = dt.isoformat()
    # Step 2: Return the ISO 8601 string
    return iso_string

# Entry point: get_iso8601_string(dt: datetime) -> str

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_21txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_get_iso8601_string(dt):
    result = get_iso8601_string(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
