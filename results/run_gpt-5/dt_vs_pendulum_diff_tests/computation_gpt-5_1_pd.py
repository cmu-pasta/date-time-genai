
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def exact_time_difference(dt_start: pendulum.DateTime, dt_end: pendulum.DateTime) -> pendulum.Duration:
    """
    Calculate the exact signed time difference between two timestamps,
    correctly accounting for daylight saving time by normalizing both
    timestamps to UTC before computing the difference.

    Args:
        dt_start (pendulum.DateTime): The start timestamp.
        dt_end (pendulum.DateTime): The end timestamp.

    Returns:
        pendulum.Duration: The signed duration representing dt_end - dt_start.
    """
    # Normalize both timestamps to UTC to ensure DST transitions are handled unambiguously
    start_utc = dt_start.in_timezone("UTC")
    end_utc = dt_end.in_timezone("UTC")

    # Compute signed difference (end - start). Using absolute=False preserves the sign.
    duration = end_utc.diff(start_utc, absolute=False)
    return duration

# Entry point: exact_time_difference(dt_start: pendulum.DateTime, dt_end: pendulum.DateTime) -> pendulum.Duration

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_1_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_exact_time_difference(dt_start, dt_end):
    result = exact_time_difference(dt_start, dt_end)
    formatted_result = format_value_pd(result, dt_start, dt_end)
    log_file.write(formatted_result + "\n")
