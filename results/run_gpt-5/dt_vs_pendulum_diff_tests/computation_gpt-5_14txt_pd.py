
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def add_business_days(start_date: pendulum.Date, n: int) -> pendulum.Date:
    """
    Return the date that is exactly n business days after start_date.
    Business days are Monday (0) through Friday (4).
    If n is 0, the start_date is returned unchanged.
    """
    if n <= 0:
        return start_date

    current = start_date
    added = 0

    while added < n:
        current = current.add(days=1)
        # Monday=0 ... Sunday=6
        if 0 <= current.weekday() <= 4:
            added += 1

    return current

# Entry point: add_business_days(start_date: pendulum.Date, n: int) -> pendulum.Date

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_14txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), timestamp_strategy())
def test_add_business_days(start_date, n):
    result = add_business_days(start_date, n)
    formatted_result = format_value_pd(result, start_date, n)
    log_file.write(formatted_result + "\n")
