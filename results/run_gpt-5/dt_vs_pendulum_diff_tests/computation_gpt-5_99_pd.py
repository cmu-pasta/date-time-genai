
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def to_decimal_time(t: pendulum.Time) -> float:
    """
    Convert a pendulum.Time to its decimal time representation in hours.
    Example: 13:30:00 -> 13.5
    """
    hours = t.hour
    minutes = t.minute
    seconds = t.second
    microseconds = t.microsecond

    # Convert the time to decimal hours
    decimal_hours = (
        hours
        + minutes / 60.0
        + seconds / 3600.0
        + microseconds / 3_600_000_000.0
    )
    return float(decimal_hours)

# Entry point: to_decimal_time(t: pendulum.Time) -> float

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_99_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy())
def test_to_decimal_time(t):
    result = to_decimal_time(t)
    formatted_result = format_value_pd(result, t)
    log_file.write(formatted_result + "\n")
