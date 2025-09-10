
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import time
def is_time_in_recurring_interval(target_time: time, interval_start: time, interval_end: time) -> bool:
    """
    Determine if target_time falls within the recurring interval specified by interval_start and interval_end.
    Handles intervals that either do or do not wrap around midnight.
    """
    if interval_start < interval_end:
        # Interval does not cross midnight
        return interval_start <= target_time < interval_end
    else:
        # Interval wraps around midnight
        return target_time >= interval_start or target_time < interval_end

# Entry point: is_time_in_recurring_interval(target_time: time, interval_start: time, interval_end: time) -> bool

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
log_file = open(os.path.join(".logs/diff_test_logs", "log_computation_gpt-41_86txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy(), time_strategy(), time_strategy())
def test_is_time_in_recurring_interval(target_time, interval_start, interval_end):
    result = is_time_in_recurring_interval(target_time, interval_start, interval_end)
    formatted_result = format_value_dt(result, target_time, interval_start, interval_end)
    log_file.write(formatted_result + "\n")
