
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date
def days_since_reference(moment: datetime, reference_date: date) -> int:
    """
    Convert a datetime to the number of days since a reference date.
    Returns a signed integer: positive if moment is after the reference_date,
    negative if before, and zero if on the same calendar date.
    """
    return (moment.date() - reference_date).days

# Entry point: days_since_reference(moment: datetime, reference_date: date) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_76_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), date_strategy())
def test_days_since_reference(moment, reference_date):
    result = days_since_reference(moment, reference_date)
    formatted_result = format_value_dt(result, moment, reference_date)
    log_file.write(formatted_result + "\n")
