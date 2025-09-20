
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def convert_12h_to_24h(t12: pendulum.Time, is_pm: bool) -> pendulum.Time:
    """
    Convert a 12-hour time to 24-hour time using Pendulum types only.

    Parameters:
    - t12: pendulum.Time representing a 12-hour clock time (hour field interpreted as 1-12, with 12 representing 12 o'clock).
    - is_pm: bool indicating whether the time is PM (True) or AM (False).

    Returns:
    - pendulum.Time in 24-hour format, preserving minutes, seconds, microseconds, and timezone.
    """
    # Normalize hour into 0-11 range, where 12 becomes 0
    base_hour = t12.hour % 12
    # Add 12 hours if PM, otherwise keep as is for AM
    hour_24 = base_hour + (12 if is_pm else 0)

    return pendulum.time(
        hour_24,
        t12.minute,
        t12.second,
        t12.microsecond,
        tz=t12.tz
    )

# Entry point: convert_12h_to_24h(t12: pendulum.Time, is_pm: bool) -> pendulum.Time

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_22_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy(), bool_strategy())
def test_convert_12h_to_24h(t12, is_pm):
    result = convert_12h_to_24h(t12, is_pm)
    formatted_result = format_value_pd(result, t12, is_pm)
    log_file.write(formatted_result + "\n")
