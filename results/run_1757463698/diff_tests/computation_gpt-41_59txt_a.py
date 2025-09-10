
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def parse_time_with_timezone(time_string: str) -> datetime:
    """
    Parses a time string with timezone offset (ISO 8601 format)
    and returns a timezone-aware datetime object.
    """
    # Step 1: Parse the string using fromisoformat (handles offsets like +05:30)
    dt = datetime.fromisoformat(time_string)
    
    # Step 2: Return the aware datetime object
    return dt

# Entry point: parse_time_with_timezone(time_string: str) -> datetime

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_59txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(string_strategy())
def test_parse_time_with_timezone(time_string):
    result = parse_time_with_timezone(time_string)
    formatted_result = format_value_dt(result, time_string)
    log_file.write(formatted_result + "\n")
