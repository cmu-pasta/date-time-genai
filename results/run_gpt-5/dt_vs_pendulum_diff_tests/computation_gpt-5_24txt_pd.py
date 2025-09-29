
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def working_hours_between(start: pendulum.DateTime, end: pendulum.DateTime) -> pendulum.Duration:
    """
    Calculate the working time between two datetimes excluding weekends.
    Working time includes all elapsed time on weekdays (Monday-Friday) within the interval.
    
    Inputs:
      - start: pendulum.DateTime
      - end: pendulum.DateTime
    Output:
      - pendulum.Duration representing total working time
    """
    # Ensure chronological order
    if end < start:
        start, end = end, start

    cursor = start
    total = pendulum.duration(seconds=0)

    # Process in [cursor, start_of_next_day) slices until reaching 'end'
    while cursor < end:
        start_of_next_day = cursor.start_of_day().add(days=1)
        next_boundary = end if end < start_of_next_day else start_of_next_day

        # Only count time on weekdays
        if not cursor.is_weekend():
            total += (next_boundary - cursor)

        cursor = next_boundary

    return total

# Entry point: working_hours_between(start: pendulum.DateTime, end: pendulum.DateTime) -> pendulum.Duration

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

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_24txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_working_hours_between(start, end):
    result = working_hours_between(start, end)
    formatted_result = format_value_pd(result, start, end)
    log_file.write(formatted_result + "\n")
