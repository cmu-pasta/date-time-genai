
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_time_difference_in_hours(t1: pendulum.Time, t2: pendulum.Time) -> float:
    """
    Calculate the absolute time difference in hours between two pendulum.Time objects.
    The times are anchored to the same arbitrary date to compute the difference.
    Timezones (if present on the Time objects) are respected; otherwise UTC is assumed.
    """
    # Use a fixed reference date for both times
    ref_year, ref_month, ref_day = 2000, 1, 1

    # Determine timezones (default to UTC if naive)
    tz1 = t1.tzinfo or pendulum.UTC
    tz2 = t2.tzinfo or pendulum.UTC

    # Create DateTime objects on the same reference date with respective timezones
    dt1 = pendulum.datetime(ref_year, ref_month, ref_day, t1.hour, t1.minute, t1.second, t1.microsecond, tz=tz1)
    dt2 = pendulum.datetime(ref_year, ref_month, ref_day, t2.hour, t2.minute, t2.second, t2.microsecond, tz=tz2)

    # Compute absolute difference in seconds
    diff_seconds = (dt2 - dt1).total_seconds()
    if diff_seconds < 0:
        diff_seconds = -diff_seconds

    # Convert seconds to hours (float)
    return diff_seconds / 3600.0

# Entry point: calculate_time_difference_in_hours(t1: pendulum.Time, t2: pendulum.Time) -> float

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_18txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy(), time_strategy())
def test_calculate_time_difference_in_hours(t1, t2):
    result = calculate_time_difference_in_hours(t1, t2)
    formatted_result = format_value_pd(result, t1, t2)
    log_file.write(formatted_result + "\n")
