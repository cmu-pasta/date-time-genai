
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def convert_to_12h(dt: pendulum.DateTime) -> pendulum.Time:
    """
    Convert a pendulum.DateTime from 24-hour format to a 12-hour clock Time.
    The returned pendulum.Time holds the 12-hour clock hour (1-12) with the same minutes,
    seconds, and microseconds as the input. AM/PM can be determined by dt.hour >= 12.
    """
    h24 = dt.hour
    m = dt.minute
    s = dt.second
    us = dt.microsecond

    # Map 24-hour to 12-hour clock: 0 -> 12 (AM), 13 -> 1 (PM), 12 -> 12 (PM)
    h12 = ((h24 + 11) % 12) + 1

    return pendulum.time(h12, m, s, us)

# Entry point: convert_to_12h(dt: pendulum.DateTime) -> pendulum.Time

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_46_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_convert_to_12h(dt):
    result = convert_to_12h(dt)
    formatted_result = format_value_pd(result, dt)
    log_file.write(formatted_result + "\n")
