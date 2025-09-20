
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def next_new_moon(after: pendulum.DateTime) -> pendulum.DateTime:
    """
    Compute the date and time of the next new moon strictly after the given datetime.
    Uses an average synodic month approximation relative to a known reference new moon.

    Input:  after (pendulum.DateTime) - the moment after which to find the next new moon
    Output: pendulum.DateTime - the UTC datetime of the next new moon
    """
    # Step 1: Reference new moon (UTC): 2000-01-06 18:14:00 UTC
    ref_new_moon = pendulum.datetime(2000, 1, 6, 18, 14, 0, tz="UTC")

    # Step 2: Average synodic month length in microseconds (integer arithmetic)
    # 1 day = 86_400 seconds = 86_400_000_000 microseconds
    synodic_days = 29.530588853
    synodic_us = int(round(synodic_days * 86_400_000_000))  # microseconds per synodic month

    # Helper to convert a DateTime to UTC microseconds since epoch using pendulum only
    def to_utc_microseconds(dt: pendulum.DateTime) -> int:
        dt_utc = dt.in_timezone("UTC")
        return dt_utc.int_timestamp * 1_000_000 + dt_utc.microsecond

    # Step 3: Compute elapsed microseconds since the reference
    after_us = to_utc_microseconds(after)
    ref_us = to_utc_microseconds(ref_new_moon)
    diff_us = after_us - ref_us

    # Step 4: Determine the number of lunations to add to reach the next new moon strictly after 'after'
    if diff_us < 0:
        # Input is before the reference; the next new moon is the reference itself
        n = 0
    else:
        # Number of complete lunations that have fully elapsed
        complete = diff_us // synodic_us
        # Move to the next lunation to ensure result is strictly after 'after'
        n = complete + 1

    # Step 5: Compute the next new moon timestamp in microseconds
    next_new_moon_us = ref_us + n * synodic_us

    # Step 6: Convert microseconds back to a pendulum.DateTime in UTC
    next_sec = next_new_moon_us // 1_000_000
    next_micro = next_new_moon_us % 1_000_000
    next_dt = pendulum.from_timestamp(next_sec, tz="UTC").replace(microsecond=next_micro)

    return next_dt

# Entry point: next_new_moon(after: pendulum.DateTime) -> pendulum.DateTime

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_74_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_next_new_moon(after):
    result = next_new_moon(after)
    formatted_result = format_value_pd(result, after)
    log_file.write(formatted_result + "\n")
