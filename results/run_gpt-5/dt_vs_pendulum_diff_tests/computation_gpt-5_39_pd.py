
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_age_in_days(birth_date: pendulum.Date, reference_date: pendulum.Date) -> int:
    """
    Calculate the total age in days between a birth date and a reference date.

    Args:
        birth_date (pendulum.Date): The birth date.
        reference_date (pendulum.Date): The reference date.

    Returns:
        int: The total number of days between the two dates (non-negative).
    """
    duration: pendulum.Duration = reference_date - birth_date
    total_days: int = abs(duration.in_days())
    return total_days

# Entry point: calculate_age_in_days(birth_date: pendulum.Date, reference_date: pendulum.Date) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_39_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_calculate_age_in_days(birth_date, reference_date):
    result = calculate_age_in_days(birth_date, reference_date)
    formatted_result = format_value_pd(result, birth_date, reference_date)
    log_file.write(formatted_result + "\n")
