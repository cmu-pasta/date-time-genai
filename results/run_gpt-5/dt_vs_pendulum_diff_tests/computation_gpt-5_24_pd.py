
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def working_hours_between(start: pendulum.DateTime, end: pendulum.DateTime) -> pendulum.Duration:
    """
    Calculate the working time between two datetimes, counting only weekday hours (Mon-Fri),
    and excluding all weekend time. Returns a pendulum.Duration.
    """
    # Ensure chronological order
    if start > end:
        start, end = end, start

    total = pendulum.duration()  # zero duration

    # If same calendar day
    if start.date() == end.date():
        if start.weekday() <= 4:  # Mon-Fri -> 0..4
            total = total + (end - start)
        return total

    # First day portion (from start to midnight next day) if it's a weekday
    if start.weekday() <= 4:
        end_of_first = start.start_of('day').add(days=1)
        chunk_end = end if end < end_of_first else end_of_first
        total = total + (chunk_end - start)

    # Full intermediate days (from the day after start's day up to the day before end's day)
    day_cursor = start.start_of('day').add(days=1)
    last_midnight = end.start_of('day')
    while day_cursor < last_midnight:
        if day_cursor.weekday() <= 4:
            total = total + pendulum.duration(days=1)
        day_cursor = day_cursor.add(days=1)

    # Last day portion (from midnight to end) if it's a weekday
    if end.weekday() <= 4 and end.start_of('day') < end:
        total = total + (end - end.start_of('day'))

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_24_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_working_hours_between(start, end):
    result = working_hours_between(start, end)
    formatted_result = format_value_pd(result, start, end)
    log_file.write(formatted_result + "\n")
