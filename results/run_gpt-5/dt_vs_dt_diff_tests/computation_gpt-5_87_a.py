
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime
def calculate_nanoseconds_between(ts1: datetime, ts2: datetime) -> int:
    # Step 1: Compute the timedelta difference
    delta = ts2 - ts1

    # Step 2: Convert the timedelta to nanoseconds using integer math
    # Note: datetime supports microsecond precision; resulting nanoseconds will be multiples of 1,000.
    total_nanoseconds = (
        delta.days * 86_400_000_000_000  # 24*60*60*1e9
        + delta.seconds * 1_000_000_000
        + delta.microseconds * 1_000
    )

    # Step 3: Return the absolute nanoseconds as an integer
    return abs(total_nanoseconds)

# Entry point: calculate_nanoseconds_between(ts1: datetime, ts2: datetime) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_87_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_nanoseconds_between(ts1, ts2):
    result = calculate_nanoseconds_between(ts1, ts2)
    formatted_result = format_value_dt(result, ts1, ts2)
    log_file.write(formatted_result + "\n")
