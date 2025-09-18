
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def milliseconds_in_duration(dur: pendulum.Duration) -> int:
    """
    Calculate the number of milliseconds in the given pendulum.Duration.

    Args:
        dur: A pendulum.Duration representing the time span.

    Returns:
        An integer representing the total number of milliseconds in the duration.
    """
    # Convert total seconds (including fractional part) to milliseconds and truncate toward zero.
    return int(dur.total_seconds() * 1000)

# Entry point: milliseconds_in_duration(dur: pendulum.Duration) -> int

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_81txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(duration_strategy())
def test_milliseconds_in_duration(dur):
    result = milliseconds_in_duration(dur)
    formatted_result = format_value_pd(result, dur)
    log_file.write(formatted_result + "\n")
