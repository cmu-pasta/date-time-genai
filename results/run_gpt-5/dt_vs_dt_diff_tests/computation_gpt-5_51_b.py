
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def total_minutes_between(start: datetime, end: datetime) -> float:
    """
    Calculate the total minutes in the period between two datetime values.

    Args:
        start (datetime): The starting datetime.
        end (datetime): The ending datetime.

    Returns:
        float: The absolute total minutes between the two datetimes, including fractional minutes.
    """
    delta = end - start
    minutes = abs(delta.total_seconds() / 60.0)
    return minutes

# Entry point: total_minutes_between(start: datetime, end: datetime) -> float

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_51_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_total_minutes_between(start, end):
    result = total_minutes_between(start, end)
    formatted_result = format_value_dt(result, start, end)
    log_file.write(formatted_result + "\n")
