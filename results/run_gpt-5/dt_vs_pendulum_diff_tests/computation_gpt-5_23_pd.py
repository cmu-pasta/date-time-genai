
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def next_full_moon(after: pendulum.DateTime) -> pendulum.DateTime:
    # Synodic month (mean time between full moons) in days
    synodic_days = 29.530588853

    # Known reference full moon: 2019-01-21 05:16:00 UTC (Total lunar eclipse full moon)
    reference_full_moon_utc = pendulum.datetime(2019, 1, 21, 5, 16, 0, tz="UTC")

    # Preserve the original timezone to return the result in the same timezone
    original_tz: pendulum.Timezone = after.timezone

    # Normalize input to UTC for calculation
    after_utc: pendulum.DateTime = after.in_timezone("UTC")

    # Compute elapsed time in days since the reference full moon
    delta_seconds: float = after_utc.float_timestamp - reference_full_moon_utc.float_timestamp
    delta_days: float = delta_seconds / 86400.0

    # Compute remaining days until the next full moon strictly after 'after'
    remainder: float = delta_days % synodic_days
    remaining_days: float = synodic_days if remainder == 0 else (synodic_days - remainder)

    # Next full moon in UTC
    next_full_moon_utc: pendulum.DateTime = after_utc + pendulum.duration(days=remaining_days)

    # Return in the original timezone
    return next_full_moon_utc.in_timezone(original_tz)

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_23_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_next_full_moon(after):
    result = next_full_moon(after)
    formatted_result = format_value_pd(result, after)
    log_file.write(formatted_result + "\n")
