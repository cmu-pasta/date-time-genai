
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_midpoint_datetime(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> pendulum.DateTime:
    """
    Compute the midpoint datetime between two pendulum.DateTime instances.

    Args:
        dt1: A pendulum.DateTime instance.
        dt2: A pendulum.DateTime instance.

    Returns:
        A pendulum.DateTime representing the midpoint between dt1 and dt2.
    """
    # Ensure we work from the earlier instant forward
    if dt1 <= dt2:
        earlier, later = dt1, dt2
    else:
        earlier, later = dt2, dt1

    # Compute half the duration between the two datetimes
    half_delta: pendulum.Duration = later.diff(earlier, absolute=True) / 2

    # Midpoint is earlier plus half the duration
    midpoint: pendulum.DateTime = earlier + half_delta
    return midpoint

# Entry point: find_midpoint_datetime(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> pendulum.DateTime

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_26txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_find_midpoint_datetime(dt1, dt2):
    result = find_midpoint_datetime(dt1, dt2)
    formatted_result = format_value_pd(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
