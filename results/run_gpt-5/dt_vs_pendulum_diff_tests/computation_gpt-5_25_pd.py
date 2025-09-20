
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def ranges_overlap(start1: pendulum.DateTime, end1: pendulum.DateTime,
                   start2: pendulum.DateTime, end2: pendulum.DateTime) -> bool:
    # Normalize the first range
    if end1 < start1:
        start1, end1 = end1, start1
    # Normalize the second range
    if end2 < start2:
        start2, end2 = end2, start2
    # Check for overlap (inclusive)
    return (start1 <= end2) and (start2 <= end1)

# Entry point: ranges_overlap(start1: pendulum.DateTime, end1: pendulum.DateTime, start2: pendulum.DateTime, end2: pendulum.DateTime) -> bool

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_25_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy(), datetime_strategy(), datetime_strategy())
def test_ranges_overlap(start1, end1, start2, end2):
    result = ranges_overlap(start1, end1, start2, end2)
    formatted_result = format_value_pd(result, start1, end1, start2, end2)
    log_file.write(formatted_result + "\n")
