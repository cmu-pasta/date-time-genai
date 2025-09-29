
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_decimal_time(t: pendulum.Time) -> float:
    """
    Convert a given pendulum.Time to its decimal hour representation.

    Example:
    13:30:00 -> 13.5
    01:15:30.500000 -> 1.258472222...
    """
    hours = t.hour
    minutes = t.minute
    seconds = t.second
    microseconds = t.microsecond

    # Convert to decimal hours with microsecond precision
    decimal_hours = (
        hours
        + minutes / 60.0
        + seconds / 3600.0
        + microseconds / 3_600_000_000.0
    )
    return float(decimal_hours)

# Entry point: calculate_decimal_time(t: pendulum.Time) -> float

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_99txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy())
def test_calculate_decimal_time(t):
    result = calculate_decimal_time(t)
    formatted_result = format_value_pd(result, t)
    log_file.write(formatted_result + "\n")
