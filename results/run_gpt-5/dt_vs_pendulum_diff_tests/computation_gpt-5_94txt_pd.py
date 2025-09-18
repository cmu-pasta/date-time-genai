
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def datetime_to_mjd(dt: pendulum.DateTime) -> float:
    """
    Convert a pendulum.DateTime to Modified Julian Date (MJD).
    MJD = JD - 2400000.5
    Using relation: JD = 2440587.5 + (unix_seconds / 86400)
    Therefore: MJD = 40587.0 + (unix_seconds / 86400)
    """
    # Ensure the datetime is in UTC for a consistent epoch reference
    dt_utc = dt.in_timezone("UTC")
    
    # Get Unix timestamp in seconds as a float (includes fractional seconds)
    unix_seconds: float = dt_utc.float_timestamp
    
    # Convert to Modified Julian Date
    mjd: float = unix_seconds / 86400.0 + 40587.0
    
    return mjd

# Entry point: datetime_to_mjd(dt: pendulum.DateTime) -> float

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_94txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_datetime_to_mjd(dt):
    result = datetime_to_mjd(dt)
    formatted_result = format_value_pd(result, dt)
    log_file.write(formatted_result + "\n")
