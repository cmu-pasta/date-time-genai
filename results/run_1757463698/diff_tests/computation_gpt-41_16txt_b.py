
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def previous_weekday_before(reference_date: date, target_weekday: int) -> date:
    """
    Given a reference date and a target_weekday (0=Monday,...,6=Sunday),
    return the date of the previous occurrence of target_weekday before the reference date.
    """
    # Step 1: Get the weekday of the reference date
    ref_weekday = reference_date.weekday()
    # Step 2: Calculate days to subtract
    days_ago = (ref_weekday - target_weekday) % 7
    # Step 3: If the reference date is the target weekday, go back 7 days (to the prior week)
    if days_ago == 0:
        days_ago = 7
    # Step 4: Compute the previous occurrence
    prev_date = reference_date - timedelta(days=days_ago)
    # Step 5: Return the previous weekday date
    return prev_date

# Entry point: previous_weekday_before(reference_date: date, target_weekday: int) -> date

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_16txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), timestamp_strategy())
def test_previous_weekday_before(reference_date, target_weekday):
    result = previous_weekday_before(reference_date, target_weekday)
    formatted_result = format_value_dt(result, reference_date, target_weekday)
    log_file.write(formatted_result + "\n")
