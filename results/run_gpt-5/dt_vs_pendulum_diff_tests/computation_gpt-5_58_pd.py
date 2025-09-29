
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def convert_unix_to_windows_filetime(unix_seconds: float) -> int:
    # Step 1: Define epochs in UTC using pendulum
    unix_epoch = pendulum.datetime(1970, 1, 1, tz="UTC")
    windows_epoch = pendulum.datetime(1601, 1, 1, tz="UTC")
    
    # Step 2: Compute the offset between epochs in seconds
    epoch_offset_seconds = unix_epoch.diff(windows_epoch).in_seconds()
    # Note: diff(a).in_seconds() returns the whole-second difference between 'self' and 'a'
    # Here, it's 11644473600 seconds from 1601-01-01 to 1970-01-01.

    # Step 3: Convert Unix seconds to Windows FILETIME ticks (100-nanosecond intervals)
    # FILETIME ticks = (seconds since 1601-01-01) * 10_000_000
    total_seconds_since_windows_epoch = unix_seconds + epoch_offset_seconds
    filetime_ticks = int(total_seconds_since_windows_epoch * 10_000_000)
    
    # Step 4: Return the integer number of FILETIME ticks
    return filetime_ticks

# Entry point: convert_unix_to_windows_filetime(unix_seconds: float) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_58_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(float_strategy())
def test_convert_unix_to_windows_filetime(unix_seconds):
    result = convert_unix_to_windows_filetime(unix_seconds)
    formatted_result = format_value_pd(result, unix_seconds)
    log_file.write(formatted_result + "\n")
