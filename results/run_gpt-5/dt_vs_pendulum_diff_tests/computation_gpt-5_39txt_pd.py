
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_age_in_total_days(birth_dt: pendulum.DateTime, reference_dt: pendulum.DateTime) -> int:
    """
    Calculate the age in total days between a birth datetime and a reference datetime.

    Args:
        birth_dt (pendulum.DateTime): The birth date and time.
        reference_dt (pendulum.DateTime): The reference date and time.

    Returns:
        int: The non-negative total number of days between the two datetimes.
    """
    # Compute signed difference in days (negative if reference is before birth)
    days = reference_dt.diff(birth_dt, absolute=False).in_days()
    # Age cannot be negative
    return max(0, days)

# Entry point: calculate_age_in_total_days(birth_dt: pendulum.DateTime, reference_dt: pendulum.DateTime) -> int

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_39txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_age_in_total_days(birth_dt, reference_dt):
    result = calculate_age_in_total_days(birth_dt, reference_dt)
    formatted_result = format_value_pd(result, birth_dt, reference_dt)
    log_file.write(formatted_result + "\n")
