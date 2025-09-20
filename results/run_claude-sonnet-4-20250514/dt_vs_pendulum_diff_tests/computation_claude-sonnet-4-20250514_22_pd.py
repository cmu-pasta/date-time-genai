
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def convert_12_to_24_hour(hour: int, minute: int, second: int, is_pm: bool) -> pendulum.Time:
    # Step 1: Convert 12-hour format to 24-hour format
    if is_pm:
        # PM case: add 12 to hour, except for 12 PM which stays 12
        if hour == 12:
            hour_24 = 12
        else:
            hour_24 = hour + 12
    else:
        # AM case: keep hour as is, except 12 AM becomes 0
        if hour == 12:
            hour_24 = 0
        else:
            hour_24 = hour
    
    # Step 2: Create and return pendulum.Time object in 24-hour format
    return pendulum.Time(hour_24, minute, second)

# Entry point: convert_12_to_24_hour(hour: int, minute: int, second: int, is_pm: bool) -> pendulum.Time

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_22_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy(), bool_strategy())
def test_convert_12_to_24_hour(hour, minute, second, is_pm):
    result = convert_12_to_24_hour(hour, minute, second, is_pm)
    formatted_result = format_value_pd(result, hour, minute, second, is_pm)
    log_file.write(formatted_result + "\n")
