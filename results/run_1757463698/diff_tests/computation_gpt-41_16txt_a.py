
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def previous_weekday(before_date: date, target_weekday: int) -> date:
    """
    Finds the previous occurrence of the specified weekday before the given date.
    :param before_date: The reference date as a date object.
    :param target_weekday: The target weekday as an integer (Monday=0, Sunday=6).
    :return: The previous occurrence of the specified weekday as a date object.
    """
    # Step 1: Determine the current weekday
    current_weekday = before_date.weekday()
    
    # Step 2: Calculate days to subtract; ensure result is not today even if matches
    days_back = (current_weekday - target_weekday) % 7 or 7  # if same day, go 7 days back

    # Step 3: Compute the previous weekday date
    prev_date = before_date - timedelta(days=days_back)
    
    # Step 4: Return the previous weekday date
    return prev_date

# Entry point: previous_weekday(before_date: date, target_weekday: int) -> date

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_16txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), timestamp_strategy())
def test_previous_weekday(before_date, target_weekday):
    result = previous_weekday(before_date, target_weekday)
    formatted_result = format_value_dt(result, before_date, target_weekday)
    log_file.write(formatted_result + "\n")
