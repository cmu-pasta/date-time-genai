
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def datetime_to_iso8601(dt: datetime) -> str:
    """
    Convert a datetime to an ISO 8601 formatted string.
    """
    # Step 1: Use the built-in isoformat method for ISO 8601 representation
    iso_string = dt.isoformat()
    
    # Step 2: Return the ISO 8601 string
    return iso_string

# Entry point: datetime_to_iso8601(dt: datetime) -> str

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_28_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_datetime_to_iso8601(dt):
    result = datetime_to_iso8601(dt)
    formatted_result = format_value_dt(result, dt)
    log_file.write(formatted_result + "\n")
