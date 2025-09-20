
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_seconds_difference(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> int:
    # Calculate the difference between the two DateTime objects.
    # The diff() method returns a pendulum.Duration object.
    duration_difference = dt2.diff(dt1)
    
    # Get the total number of seconds from the duration.
    # Use abs() to ensure the result is a positive integer, regardless of the order of dt1 and dt2.
    total_seconds = abs(duration_difference.in_seconds())
    
    return total_seconds

# Entry point: calculate_seconds_difference(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_9_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_seconds_difference(dt1, dt2):
    result = calculate_seconds_difference(dt1, dt2)
    formatted_result = format_value_pd(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
