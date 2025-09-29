
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def check_date_ranges_overlap(range1_start: pendulum.DateTime, range1_end: pendulum.DateTime, 
                             range2_start: pendulum.DateTime, range2_end: pendulum.DateTime) -> bool:
    # Step 1: Check if the ranges overlap
    # Two ranges overlap if: range1_start <= range2_end AND range2_start <= range1_end
    overlap = range1_start <= range2_end and range2_start <= range1_end
    
    # Step 2: Return the boolean result
    return overlap

# Entry point: check_date_ranges_overlap(range1_start: pendulum.DateTime, range1_end: pendulum.DateTime, range2_start: pendulum.DateTime, range2_end: pendulum.DateTime) -> bool

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
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_25_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy(), datetime_strategy(), datetime_strategy())
def test_check_date_ranges_overlap(range1_start, range1_end, range2_start, range2_end):
    result = check_date_ranges_overlap(range1_start, range1_end, range2_start, range2_end)
    formatted_result = format_value_pd(result, range1_start, range1_end, range2_start, range2_end)
    log_file.write(formatted_result + "\n")
