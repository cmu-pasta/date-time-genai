
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def ranges_overlap(start1: datetime, end1: datetime, start2: datetime, end2: datetime) -> bool:
    """
    Determine if two datetime ranges overlap.
    The ranges are considered closed intervals [start, end], so touching endpoints count as overlap.

    Parameters:
    - start1: datetime - Start of first range
    - end1: datetime   - End of first range
    - start2: datetime - Start of second range
    - end2: datetime   - End of second range

    Returns:
    - bool: True if the ranges overlap, False otherwise.
    """

    # Normalize the ranges to ensure start <= end
    if start1 > end1:
        start1, end1 = end1, start1
    if start2 > end2:
        start2, end2 = end2, start2

    # Overlap exists if the latest start is <= the earliest end
    return (start1 <= end2) and (start2 <= end1)

# Entry point: ranges_overlap(start1: datetime, end1: datetime, start2: datetime, end2: datetime) -> bool

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

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_25txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy(), datetime_strategy(), datetime_strategy())
def test_ranges_overlap(start1, end1, start2, end2):
    result = ranges_overlap(start1, end1, start2, end2)
    formatted_result = format_value_dt(result, start1, end1, start2, end2)
    log_file.write(formatted_result + "\n")
