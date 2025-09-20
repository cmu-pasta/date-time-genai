
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def convert_to_mjd(dt: pendulum.DateTime) -> float:
    # Julian Date (JD) of the Unix epoch (Jan 1, 1970, 00:00:00 UTC)
    JD_UNIX_EPOCH = 2440587.5
    
    # Seconds in a day
    SECONDS_IN_DAY = 86400.0

    # Get the Unix timestamp (seconds since Unix epoch)
    timestamp_seconds = dt.timestamp()

    # Calculate the number of days (and fractional days) since the Unix epoch
    days_since_unix_epoch = timestamp_seconds / SECONDS_IN_DAY

    # Calculate the Julian Date (JD)
    julian_date = JD_UNIX_EPOCH + days_since_unix_epoch

    # Calculate the Modified Julian Date (MJD)
    # MJD = JD - 2400000.5
    modified_julian_date = julian_date - 2400000.5
    
    return modified_julian_date

# Entry point: convert_to_mjd(dt: pendulum.DateTime) -> float

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_94_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_convert_to_mjd(dt):
    result = convert_to_mjd(dt)
    formatted_result = format_value_pd(result, dt)
    log_file.write(formatted_result + "\n")
