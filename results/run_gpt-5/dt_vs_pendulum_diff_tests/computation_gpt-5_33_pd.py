
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def minutes_between_times(t1: pendulum.Time, t2: pendulum.Time) -> int:
    # Step 1: Convert both times to total seconds from midnight
    s1 = t1.hour * 3600 + t1.minute * 60 + t1.second
    s2 = t2.hour * 3600 + t2.minute * 60 + t2.second

    # Step 2: Compute absolute difference in seconds
    diff_seconds = abs(s2 - s1)

    # Step 3: Convert seconds to whole minutes
    diff_minutes = diff_seconds // 60

    # Step 4: Return the integer number of minutes
    return int(diff_minutes)

# Entry point: minutes_between_times(t1: pendulum.Time, t2: pendulum.Time) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_33_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy(), time_strategy())
def test_minutes_between_times(t1, t2):
    result = minutes_between_times(t1, t2)
    formatted_result = format_value_pd(result, t1, t2)
    log_file.write(formatted_result + "\n")
