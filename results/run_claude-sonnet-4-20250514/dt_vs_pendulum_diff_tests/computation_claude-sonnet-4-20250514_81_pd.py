
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_milliseconds(duration: pendulum.Duration) -> int:
    # Step 1: Get the total duration in seconds as a float
    total_seconds = duration.total_seconds()
    
    # Step 2: Convert seconds to milliseconds by multiplying by 1000
    milliseconds = total_seconds * 1000
    
    # Step 3: Return the result as an integer
    return int(milliseconds)

# Entry point: calculate_milliseconds(duration: pendulum.Duration) -> int

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_81_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(duration_strategy())
def test_calculate_milliseconds(duration):
    result = calculate_milliseconds(duration)
    formatted_result = format_value_pd(result, duration)
    log_file.write(formatted_result + "\n")
