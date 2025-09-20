
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_nanoseconds_difference(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> int:
    # Step 1: Calculate the difference between the two timestamps
    difference = dt2.diff(dt1)
    
    # Step 2: Convert the difference to nanoseconds
    # total_seconds() returns a float, multiply by 1e9 to get nanoseconds
    nanoseconds = int(difference.total_seconds() * 1_000_000_000)
    
    # Step 3: Return the absolute value to ensure positive result
    return abs(nanoseconds)

# Entry point: calculate_nanoseconds_difference(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> int

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_87_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_nanoseconds_difference(dt1, dt2):
    result = calculate_nanoseconds_difference(dt1, dt2)
    formatted_result = format_value_pd(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
