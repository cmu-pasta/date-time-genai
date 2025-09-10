
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def parse_datetime_string(date_string: str, format_string: str) -> datetime:
    # Step 1: Parse the datetime string using the provided custom format
    parsed_datetime = datetime.strptime(date_string, format_string)
    
    # Step 2: Return the parsed datetime object
    return parsed_datetime

# Entry point: parse_datetime_string(date_string: str, format_string: str) -> datetime

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_26txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(string_strategy(), string_strategy())
def test_parse_datetime_string(date_string, format_string):
    result = parse_datetime_string(date_string, format_string)
    formatted_result = format_value_dt(result, date_string, format_string)
    log_file.write(formatted_result + "\n")
