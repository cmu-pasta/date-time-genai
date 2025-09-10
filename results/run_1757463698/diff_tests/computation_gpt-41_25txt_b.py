
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_nanoseconds_difference(dt1: datetime, dt2: datetime) -> int:
    """
    Calculate the absolute difference in nanoseconds between two datetime objects.
    """
    # Step 1: Calculate the absolute difference as a timedelta object
    delta = abs(dt2 - dt1)
    
    # Step 2: Compute the total nanoseconds from timedelta attributes
    total_nanoseconds = (
        delta.days * 24 * 60 * 60 * 1_000_000_000 +
        delta.seconds * 1_000_000_000 +
        delta.microseconds * 1_000
    )
    # Step 3: Return the result as an integer
    return total_nanoseconds

# Entry point: calculate_nanoseconds_difference(dt1: datetime, dt2: datetime) -> int

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_25txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_nanoseconds_difference(dt1, dt2):
    result = calculate_nanoseconds_difference(dt1, dt2)
    formatted_result = format_value_dt(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
