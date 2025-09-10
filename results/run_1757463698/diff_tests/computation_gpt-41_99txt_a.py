
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time
def max_time_in_a_day(is_24_hour_format: bool) -> time:
    """
    Returns the maximum possible time in a day according to the clock format.
    
    Args:
        is_24_hour_format (bool): True for 24-hour format, False for 12-hour format.
    
    Returns:
        time: The maximum representable time in a day as a datetime.time object.
    """
    # For both 24-hour and 12-hour clocks, the latest time in a day is 23:59:59.999999
    # The difference is only in display format, not the value stored by datetime.time
    return time(23, 59, 59, 999999)

# Entry point: max_time_in_a_day(is_24_hour_format: bool) -> time

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_99txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(bool_strategy())
def test_max_time_in_a_day(is_24_hour_format):
    result = max_time_in_a_day(is_24_hour_format)
    formatted_result = format_value_dt(result, is_24_hour_format)
    log_file.write(formatted_result + "\n")
