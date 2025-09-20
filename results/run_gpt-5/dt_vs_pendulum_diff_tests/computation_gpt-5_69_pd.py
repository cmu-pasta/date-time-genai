
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def timezone_aware_difference(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> pendulum.Duration:
    """
    Calculate the time difference between two pendulum.DateTime values while
    accounting for their respective time zones. The result preserves the sign
    (dt2 - dt1) and is returned as a pendulum.Duration.
    """
    # Step 1: Normalize both datetimes to UTC to account for timezone offsets and DST
    dt1_utc: pendulum.DateTime = dt1.in_timezone("UTC")
    dt2_utc: pendulum.DateTime = dt2.in_timezone("UTC")
    
    # Step 2: Compute the difference as a pendulum.Duration (signed)
    difference: pendulum.Duration = dt2_utc - dt1_utc
    
    # Step 3: Return the duration
    return difference

# Entry point: timezone_aware_difference(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> pendulum.Duration

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_69_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_timezone_aware_difference(dt1, dt2):
    result = timezone_aware_difference(dt1, dt2)
    formatted_result = format_value_pd(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
