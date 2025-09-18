
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def count_weekends_between(start: pendulum.Date, end: pendulum.Date) -> int:
    """
    Counts the number of weekend days (Saturdays and Sundays) between two dates, inclusive.
    Inputs: start, end - pendulum.Date
    Output: int - number of weekend days
    """
    # Normalize order to ensure start <= end
    if start > end:
        start, end = end, start

    # Total days inclusive
    total_days = end.diff(start).in_days() + 1  # inclusive of both endpoints

    # Count weekend days from complete weeks
    full_weeks = total_days // 7
    weekend_days = full_weeks * 2  # Each full week has Saturday and Sunday

    # Count weekend days in the remaining partial week
    remaining_days = total_days % 7
    start_dow = start.day_of_week  # Monday=0, ..., Sunday=6

    # Iterate up to 6 days for the remainder
    for i in range(remaining_days):
        dow = (start_dow + i) % 7
        if dow == 5 or dow == 6:  # Saturday=5, Sunday=6
            weekend_days += 1

    return weekend_days

# Entry point: count_weekends_between(start: pendulum.Date, end: pendulum.Date) -> int

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_15txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_count_weekends_between(start, end):
    result = count_weekends_between(start, end)
    formatted_result = format_value_pd(result, start, end)
    log_file.write(formatted_result + "\n")
