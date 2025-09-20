
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_work_weeks_between(start: pendulum.Date, end: pendulum.Date) -> int:
    # Ensure chronological order
    if start > end:
        start, end = end, start

    # Total days inclusive
    total_days_inclusive = start.diff(end).in_days() + 1

    # Compute full weeks and remaining days
    full_weeks = total_days_inclusive // 7
    remaining_days = total_days_inclusive % 7

    # Weekdays from full weeks
    weekdays = full_weeks * 5

    # Count weekdays in the remaining span starting from start's weekday
    # Pendulum: Monday=0 ... Sunday=6
    start_dow = start.day_of_week
    extra_weekdays = 0
    for i in range(remaining_days):
        dow = (start_dow + i) % 7
        if dow < 5:  # Monday-Friday
            extra_weekdays += 1

    weekdays += extra_weekdays

    # Convert weekdays to whole work weeks (5 weekdays per week)
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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_57_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_calculate_work_weeks_between(start, end):
    result = calculate_work_weeks_between(start, end)
    formatted_result = format_value_pd(result, start, end)
    log_file.write(formatted_result + "\n")
