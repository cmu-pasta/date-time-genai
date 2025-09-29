
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def convert_timestamp_to_new_epoch(timestamp_value: float, source_epoch_start: pendulum.DateTime, target_epoch_start: pendulum.DateTime) -> float:
    # Step 1: Create a pendulum.DateTime object from the source timestamp and its epoch.
    # We assume timestamp_value is in seconds from the source epoch.
    absolute_datetime = source_epoch_start.add(seconds=timestamp_value)

    # Step 2: Calculate the duration from the target epoch start to this absolute datetime.
    # The difference operator (-) returns a pendulum.Duration object.
    duration_from_target_epoch = absolute_datetime - target_epoch_start
    
    # Step 3: Extract the total number of seconds from this duration.
    # This represents the timestamp in the new epoch.
    new_epoch_timestamp = duration_from_target_epoch.total_seconds()
    
    return new_epoch_timestamp

# Entry point: convert_timestamp_to_new_epoch(timestamp_value: float, source_epoch_start: pendulum.DateTime, target_epoch_start: pendulum.DateTime) -> float

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_58_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(float_strategy(), datetime_strategy(), datetime_strategy())
def test_convert_timestamp_to_new_epoch(timestamp_value, source_epoch_start, target_epoch_start):
    result = convert_timestamp_to_new_epoch(timestamp_value, source_epoch_start, target_epoch_start)
    formatted_result = format_value_pd(result, timestamp_value, source_epoch_start, target_epoch_start)
    log_file.write(formatted_result + "\n")
