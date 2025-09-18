
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_exact_time_difference(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> pendulum.Duration:
    """
    Calculates the exact time difference between two timezone-aware Pendulum DateTime objects,
    considering Daylight Saving Time transitions.

    Args:
        dt1: The first timezone-aware pendulum.DateTime object.
        dt2: The second timezone-aware pendulum.DateTime object.

    Returns:
        A pendulum.Duration object representing the exact time difference.
        The duration will be positive if dt2 is after dt1, and negative otherwise.
    """
    # Pendulum's diff() method automatically handles timezone and DST rules
    # when applied to timezone-aware DateTime objects.
    # The order dt2.diff(dt1) will yield a positive duration if dt2 is later than dt1.
    time_difference = dt2.diff(dt1)
    
    return time_difference

# Entry point: calculate_exact_time_difference(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> pendulum.Duration

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_1_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_exact_time_difference(dt1, dt2):
    result = calculate_exact_time_difference(dt1, dt2)
    formatted_result = format_value_pd(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
