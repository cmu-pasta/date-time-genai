
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
# Constants for the lunar phase computation
# Reference: Full Moon on 2018-01-02 02:24:00 UTC (widely documented)
_REFERENCE_FULL_MOON_UTC = pendulum.datetime(2018, 1, 2, 2, 24, tz="UTC")
# Mean synodic month length in days
_SYNODIC_MONTH_DAYS = 29.530588853

def next_full_moon(after: pendulum.DateTime) -> pendulum.DateTime:
    """
    Compute the date and time of the next full moon strictly after the given datetime.
    
    Parameters:
      after (pendulum.DateTime): The reference datetime.
      
    Returns:
      pendulum.DateTime: The next full moon instant in the same timezone as 'after'.
    """
    # Normalize to UTC for arithmetic
    after_utc = after.in_timezone("UTC")

    # If the reference time is not yet reached, the next full moon is the reference itself
    if after_utc < _REFERENCE_FULL_MOON_UTC:
        next_full_utc = _REFERENCE_FULL_MOON_UTC
    else:
        # Elapsed time in days since the reference full moon
        elapsed_seconds = (after_utc - _REFERENCE_FULL_MOON_UTC).total_seconds()
        elapsed_days = elapsed_seconds / 86400.0

        # Number of completed synodic cycles since the reference
        # Use floor via int() for non-negative values, then add 1 to get the next cycle
        cycles_completed = int(elapsed_days / _SYNODIC_MONTH_DAYS)
        next_cycle_index = cycles_completed + 1

        # Compute next full moon instant in UTC
        next_full_utc = _REFERENCE_FULL_MOON_UTC + pendulum.duration(days=_SYNODIC_MONTH_DAYS * next_cycle_index)

    # Return in the original timezone of the input
    return next_full_utc.in_timezone(after.timezone)

# Entry point: next_full_moon(after: pendulum.DateTime) -> pendulum.DateTime

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_23txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_next_full_moon(after):
    result = next_full_moon(after)
    formatted_result = format_value_pd(result, after)
    log_file.write(formatted_result + "\n")
