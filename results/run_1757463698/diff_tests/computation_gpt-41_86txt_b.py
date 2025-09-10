
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time
def is_time_in_recurring_interval(check_time: time, interval_start: time, interval_end: time) -> bool:
    """
    Checks if 'check_time' falls within a recurring interval defined by 'interval_start' and 'interval_end'.
    Handles intervals that may span midnight.
    """
    # If interval does not span midnight
    if interval_start <= interval_end:
        return interval_start <= check_time < interval_end
    else:
        # Interval spans midnight
        return check_time >= interval_start or check_time < interval_end

# Entry point: is_time_in_recurring_interval(check_time: time, interval_start: time, interval_end: time) -> bool

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_86txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy(), time_strategy(), time_strategy())
def test_is_time_in_recurring_interval(check_time, interval_start, interval_end):
    result = is_time_in_recurring_interval(check_time, interval_start, interval_end)
    formatted_result = format_value_dt(result, check_time, interval_start, interval_end)
    log_file.write(formatted_result + "\n")
