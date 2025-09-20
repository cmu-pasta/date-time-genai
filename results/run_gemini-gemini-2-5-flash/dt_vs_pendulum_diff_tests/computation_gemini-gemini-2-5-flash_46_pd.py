
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def get_12_hour_clock_hour(dt: pendulum.DateTime) -> int:
    """
    Converts a pendulum.DateTime object's hour component to a 12-hour format (1-12).
    Due to strict output type constraints, only the 12-hour integer is returned.
    The AM/PM indicator cannot be returned as part of a single primitive type.
    """
    # Get the hour in 24-hour format (0-23)
    hour_24 = dt.hour

    # Convert to 12-hour format (1-12)
    # If hour_24 is 0 (midnight) or 12 (noon), it should be 12.
    # Otherwise, it's hour_24 % 12.
    if hour_24 == 0 or hour_24 == 12:
        hour_12 = 12
    else:
        hour_12 = hour_24 % 12
        
    return hour_12

# Entry point: get_12_hour_clock_hour(dt: pendulum.DateTime) -> int

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_46_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_get_12_hour_clock_hour(dt):
    result = get_12_hour_clock_hour(dt)
    formatted_result = format_value_pd(result, dt)
    log_file.write(formatted_result + "\n")
