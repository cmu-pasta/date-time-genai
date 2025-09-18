
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def convert_12h_to_24h(hour_12: int, minute: int, second: int, is_pm: bool) -> pendulum.Time:
    # Validate inputs
    if not (1 <= hour_12 <= 12):
        raise ValueError("hour_12 must be in the range 1..12")
    if not (0 <= minute <= 59):
        raise ValueError("minute must be in the range 0..59")
    if not (0 <= second <= 59):
        raise ValueError("second must be in the range 0..59")
    if not isinstance(is_pm, bool):
        raise ValueError("is_pm must be a boolean")

    # Convert to 24-hour format
    if hour_12 == 12:
        hour_24 = 12 if is_pm else 0
    else:
        hour_24 = hour_12 + 12 if is_pm else hour_12

    # Return a pendulum.Time object in 24-hour format
    return pendulum.time(hour_24, minute, second)

# Entry point: convert_12h_to_24h(hour_12: int, minute: int, second: int, is_pm: bool) -> pendulum.Time

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_22txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy(), bool_strategy())
def test_convert_12h_to_24h(hour_12, minute, second, is_pm):
    result = convert_12h_to_24h(hour_12, minute, second, is_pm)
    formatted_result = format_value_pd(result, hour_12, minute, second, is_pm)
    log_file.write(formatted_result + "\n")
