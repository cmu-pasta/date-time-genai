
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def date_to_ordinal(dt: date) -> int:
    # Step 1: Use the .toordinal() method of the date object
    ordinal_number = dt.toordinal()
    
    # Step 2: Return the result as an integer
    return ordinal_number

# Entry point: date_to_ordinal(dt: date) -> int

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_54txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_date_to_ordinal(dt):
    result = date_to_ordinal(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
