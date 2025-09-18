
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_business_days(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> int:
    """
    Calculate the number of business days (Monday-Friday) between two dates.
    - The calculation is exclusive of the ending date and inclusive of the starting date when iterating day by day.
    - Time components are ignored by converting inputs to dates.
    - The result is always non-negative.
    """
    # Normalize to dates (drop time components)
    d1: pendulum.Date = dt1.date()
    d2: pendulum.Date = dt2.date()

    # Ensure d_start <= d_end
    if d1 <= d2:
        d_start, d_end = d1, d2
    else:
        d_start, d_end = d2, d1

    # Count business days from d_start (inclusive) to d_end (exclusive)
    count: int = 0
    current: pendulum.Date = d_start
    while current < d_end:
        # ISO weekday: 1=Monday, ..., 7=Sunday
        if current.isoweekday() <= 5:
            count += 1
        current = current.add(days=1)

    return count

# Entry point: calculate_business_days(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> int

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_0txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_business_days(dt1, dt2):
    result = calculate_business_days(dt1, dt2)
    formatted_result = format_value_pd(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
