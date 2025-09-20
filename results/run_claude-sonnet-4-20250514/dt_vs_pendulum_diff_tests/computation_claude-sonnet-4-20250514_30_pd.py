
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_time_since_epoch(timestamp: pendulum.DateTime) -> pendulum.Duration:
    # Step 1: Create the epoch datetime (January 1, 1970, 00:00:00 UTC)
    epoch = pendulum.parse('1970-01-01T00:00:00Z')
    
    # Step 2: Calculate the time elapsed since epoch
    elapsed_time = timestamp - epoch
    
    # Step 3: Return the elapsed time as a Duration
    return elapsed_time

# Entry point: calculate_time_since_epoch(timestamp: pendulum.DateTime) -> pendulum.Duration

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_30_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_time_since_epoch(timestamp):
    result = calculate_time_since_epoch(timestamp)
    formatted_result = format_value_pd(result, timestamp)
    log_file.write(formatted_result + "\n")
