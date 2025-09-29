
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import timedelta
def milliseconds_in_duration(duration: timedelta) -> int:
    """
    Calculate the total number of whole milliseconds in the given duration.
    """
    # Use integer arithmetic to avoid floating point inaccuracies
    total_milliseconds = (
        duration.days * 86_400_000 +      # days to milliseconds
        duration.seconds * 1_000 +        # seconds to milliseconds
        duration.microseconds // 1_000    # microseconds to milliseconds (truncated)
    )
    return total_milliseconds

# Entry point: milliseconds_in_duration(duration: timedelta) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_81_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(duration_strategy())
def test_milliseconds_in_duration(duration):
    result = milliseconds_in_duration(duration)
    formatted_result = format_value_dt(result, duration)
    log_file.write(formatted_result + "\n")
