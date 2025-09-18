
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def autumnal_equinox_date(year: int) -> pendulum.Date:
    """
    Compute the date of the autumnal equinox (September) for a given year
    using the widely used Japanese approximation formula, which is reliable
    for years in the range 1900–2099.

    Parameters:
        year (int): The Gregorian calendar year (1900–2099).

    Returns:
        pendulum.Date: The date of the autumnal equinox in September.
    """
    # Validate supported range for the approximation
    if year < 1900 or year > 2099:
        raise ValueError("Year out of supported range (1900–2099) for this approximation.")

    # Apply the approximation formula:
    # day = floor(23.2488 + 0.242194*(year - 1980) - floor((year - 1980)/4))
    a = year - 1980
    correction = a // 4  # floor((year - 1980)/4)
    value = 23.2488 + 0.242194 * a - correction
    day = int(value)  # value is positive in supported range; int() == floor() here

    # Construct and return the equinox date in September
    return pendulum.date(year, 9, day)

# Entry point: autumnal_equinox_date(year: int) -> pendulum.Date

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_53txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_autumnal_equinox_date(year):
    result = autumnal_equinox_date(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
