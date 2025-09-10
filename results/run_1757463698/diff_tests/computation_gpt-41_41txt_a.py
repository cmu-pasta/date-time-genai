
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timezone
def timestamp_to_rfc2822(ts: float) -> str:
    # Step 1: Convert the timestamp to a datetime object in UTC
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    
    # Step 2: Format the datetime as per RFC 2822
    # Example: "Fri, 21 Nov 1997 09:55:06 +0000"
    rfc2822_str = dt.strftime('%a, %d %b %Y %H:%M:%S %z')
    
    # Step 3: Return the formatted string
    return rfc2822_str

# Entry point: timestamp_to_rfc2822(ts: float) -> str

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_41txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(float_strategy())
def test_timestamp_to_rfc2822(ts):
    result = timestamp_to_rfc2822(ts)
    formatted_result = format_value_dt(result, ts)
    log_file.write(formatted_result + "\n")
