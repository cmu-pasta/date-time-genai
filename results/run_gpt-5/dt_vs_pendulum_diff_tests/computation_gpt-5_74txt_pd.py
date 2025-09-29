
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
# Mean synodic month length (days)
_SYNODIC_MONTH_DAYS: float = 29.530588853

# Reference new moon: 2000-01-06 18:14 UTC (well-known epoch)
_REF_NEW_MOON_UTC: pendulum.DateTime = pendulum.datetime(2000, 1, 6, 18, 14, tz='UTC')

def next_new_moon(after_dt: pendulum.DateTime) -> pendulum.DateTime:
    """
    Compute the date-time of the next new moon strictly after the given datetime.
    The computation uses a mean synodic month approximation from a known epoch.
    The result is returned as a pendulum.DateTime in UTC.
    """
    # Normalize input to UTC for consistent arithmetic
    dt_utc: pendulum.DateTime = after_dt.in_timezone('UTC')

    # Time difference in days from the reference new moon
    delta: pendulum.Duration = dt_utc - _REF_NEW_MOON_UTC
    diff_days: float = delta.total_seconds() / 86400.0

    # Estimate cycle index using floor division for floats
    n_cycles: int = int(diff_days // _SYNODIC_MONTH_DAYS)

    # Construct candidate new moon
    seconds_per_cycle: float = _SYNODIC_MONTH_DAYS * 86400.0
    candidate: pendulum.DateTime = _REF_NEW_MOON_UTC.add(seconds=n_cycles * seconds_per_cycle)

    # Ensure the returned new moon is strictly after the input
    if not (candidate > dt_utc):
        candidate = candidate.add(seconds=seconds_per_cycle)

    return candidate

# Entry point: next_new_moon(after_dt: pendulum.DateTime) -> pendulum.DateTime

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_74txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_next_new_moon(after_dt):
    result = next_new_moon(after_dt)
    formatted_result = format_value_pd(result, after_dt)
    log_file.write(formatted_result + "\n")
