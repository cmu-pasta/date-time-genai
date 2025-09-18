
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_age_in_seconds(birth_dt: pendulum.DateTime) -> int:
    """
    Calculate the chronological age in seconds for a given birth datetime.
    
    Parameters:
        birth_dt (pendulum.DateTime): The birth datetime.
        
    Returns:
        int: Age in seconds (non-negative).
    """
    if not isinstance(birth_dt, pendulum.DateTime):
        raise TypeError("birth_dt must be a pendulum.DateTime")

    # Use the same timezone as the birth datetime for an accurate calculation
    now = pendulum.now(tz=birth_dt.timezone)

    # Signed difference: positive if now is after birth_dt, negative otherwise
    seconds = now.diff(birth_dt, absolute=False).in_seconds()

    # Chronological age cannot be negative
    return seconds if seconds >= 0 else 0

# Entry point: calculate_age_in_seconds(birth_dt: pendulum.DateTime) -> int

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_75txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_age_in_seconds(birth_dt):
    result = calculate_age_in_seconds(birth_dt)
    formatted_result = format_value_pd(result, birth_dt)
    log_file.write(formatted_result + "\n")
