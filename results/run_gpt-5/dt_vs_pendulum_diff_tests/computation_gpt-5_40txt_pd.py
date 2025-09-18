
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def seconds_since_midnight(t: pendulum.Time) -> int:
    """
    Convert a pendulum.Time to the number of whole seconds since midnight.
    """
    # Extract components from the pendulum.Time object
    hours = t.hour
    minutes = t.minute
    seconds = t.second

    # Compute total seconds since midnight
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds

# Entry point: seconds_since_midnight(t: pendulum.Time) -> int

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_40txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy())
def test_seconds_since_midnight(t):
    result = seconds_since_midnight(t)
    formatted_result = format_value_pd(result, t)
    log_file.write(formatted_result + "\n")
