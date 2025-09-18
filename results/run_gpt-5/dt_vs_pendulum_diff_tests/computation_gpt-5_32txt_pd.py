
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_middle_date(d1: pendulum.Date, d2: pendulum.Date) -> pendulum.Date:
    """
    Find the date that falls exactly in the middle of two given pendulum.Date values.
    The midpoint is computed in UTC by averaging the midnight timestamps of both dates.
    """
    # Step 1: Normalize dates to DateTime at midnight UTC
    dt1 = pendulum.datetime(d1.year, d1.month, d1.day, tz="UTC")
    dt2 = pendulum.datetime(d2.year, d2.month, d2.day, tz="UTC")

    # Step 2: Compute the midpoint timestamp
    mid_ts = (dt1.float_timestamp + dt2.float_timestamp) / 2.0

    # Step 3: Reconstruct the midpoint DateTime and return its date component
    midpoint_dt = pendulum.from_timestamp(mid_ts, tz="UTC")
    return midpoint_dt.date()

# Entry point: find_middle_date(d1: pendulum.Date, d2: pendulum.Date) -> pendulum.Date

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_32txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), date_strategy())
def test_find_middle_date(d1, d2):
    result = find_middle_date(d1, d2)
    formatted_result = format_value_pd(result, d1, d2)
    log_file.write(formatted_result + "\n")
