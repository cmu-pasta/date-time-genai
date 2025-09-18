
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def next_leap_year_after(dt: pendulum.DateTime) -> int:
    """
    Determine the next leap year strictly after the given date.
    
    Args:
        dt: A pendulum.DateTime representing the reference date.
        
    Returns:
        An integer representing the next leap year after the given date.
    """
    year = dt.year + 1
    while True:
        # Use Pendulum to construct a date and check if that year is a leap year
        if pendulum.datetime(year, 1, 1).is_leap_year():
            return year
        year += 1

# Entry point: next_leap_year_after(dt: pendulum.DateTime) -> int

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_3txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_next_leap_year_after(dt):
    result = next_leap_year_after(dt)
    formatted_result = format_value_pd(result, dt)
    log_file.write(formatted_result + "\n")
