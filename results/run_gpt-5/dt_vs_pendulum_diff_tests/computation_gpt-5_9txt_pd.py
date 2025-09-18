
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_seconds_between(ts1: pendulum.DateTime, ts2: pendulum.DateTime) -> int:
    """
    Calculate the absolute number of seconds between two pendulum.DateTime timestamps.

    Args:
        ts1 (pendulum.DateTime): The first timestamp.
        ts2 (pendulum.DateTime): The second timestamp.

    Returns:
        int: The absolute difference in seconds between ts1 and ts2.
    """
    # Compute the duration between the two timestamps
    duration = ts2.diff(ts1)
    # Convert the duration to seconds and ensure non-negative result
    seconds = abs(duration.in_seconds())
    return seconds

# Entry point: calculate_seconds_between(ts1: pendulum.DateTime, ts2: pendulum.DateTime) -> int

def format_value_pd(*values):
    formatted_values = []

    for value in values:
        if isinstance(value, pendulum.DateTime):
            formatted_values.append(value.to_iso8601_string()[:-1])
        elif isinstance(value, pendulum.Date):
            formatted_values.append(value.to_date_string())
        elif isinstance(value, pendulum.Time):
            # Format time in the same way as datetime.time.isoformat() does
            formatted_time = (
                str(value.hour).zfill(2)
                + ":"
                + str(value.minute).zfill(2)
                + ":"
                + str(value.second).zfill(2)
            )
            if value.microsecond:
                # Padding microseconds to 6 digits
                formatted_time += "." + str(value.microsecond).zfill(6)
            formatted_values.append(formatted_time)
        elif isinstance(value, pendulum.Duration):
            formatted_values.append(str(value.total_seconds()))
        else:
            formatted_values.append(str(value))

    return ", ".join(formatted_values)

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_9txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_seconds_between(ts1, ts2):
    result = calculate_seconds_between(ts1, ts2)
    formatted_result = format_value_pd(result, ts1, ts2)
    log_file.write(formatted_result + "\n")
