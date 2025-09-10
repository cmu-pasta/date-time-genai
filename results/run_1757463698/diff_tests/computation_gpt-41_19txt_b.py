
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, datetime
def extract_quarter(dt: date) -> int:
    # Step 1: Extract the month from the date or datetime object
    month = dt.month
    # Step 2: Calculate the quarter
    quarter = ((month - 1) // 3) + 1
    # Step 3: Return the quarter number as an integer (1-4)
    return quarter

# Entry point: extract_quarter(dt: date) -> int

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_19txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_extract_quarter(dt):
    result = extract_quarter(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
