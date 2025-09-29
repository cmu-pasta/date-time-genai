
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_work_weeks_between(start: pendulum.Date, end: pendulum.Date) -> int:
    """
    Calculate the number of complete work weeks (Mon–Fri) between two dates.
    The calculation considers days in the half-open interval [start, end),
    i.e., it includes 'start' and excludes 'end'.
    """
    # Ensure chronological order
    if end < start:
        start, end = end, start

    # Total days in the range [start, end)
    total_days = end.diff(start).in_days()

    # Full weeks contribution
    full_weeks = total_days // 7
    weekdays = full_weeks * 5

    # Remaining days contribution
    rem = total_days % 7
    start_wd = start.day_of_week  # Monday=0 ... Sunday=6

    # Count weekdays in the remaining span (at most 6 iterations)
    for i in range(rem):
        if (start_wd + i) % 7 < 5:
            weekdays += 1

    # Number of complete work weeks
    work_weeks = weekdays // 5
    return work_weeks

# Entry point: calculate_work_weeks_between(start: pendulum.Date, end: pendulum.Date) -> int

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_57txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_calculate_work_weeks_between(start, end):
    result = calculate_work_weeks_between(start, end)
    formatted_result = format_value_pd(result, start, end)
    log_file.write(formatted_result + "\n")
