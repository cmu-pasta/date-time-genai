
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def lunar_age_days(dt: pendulum.DateTime) -> float:
    """
    Calculate the lunar age (days since the last new moon) for the given datetime.

    Args:
        dt (pendulum.DateTime): The datetime for which to compute the lunar age.

    Returns:
        float: Lunar age in days (0 <= age < 29.530588853).
    """
    # Synodic month length in days (mean lunar cycle)
    SYNODIC_MONTH_DAYS = 29.530588853

    # Reference new moon: 2000-01-06 18:14:00 UTC (widely used astronomical epoch)
    ref_new_moon = pendulum.datetime(2000, 1, 6, 18, 14, tz="UTC")

    # Normalize input to UTC (assume UTC if naive)
    utc = pendulum.timezone("UTC")
    dt_utc = dt.in_timezone(utc) if dt.timezone is not None else dt.replace(tzinfo=utc)

    # Compute precise elapsed days between dt and reference
    delta = dt_utc - ref_new_moon  # pendulum.Duration
    total_days = delta.total_seconds() / 86400.0

    # Lunar age is elapsed days modulo the synodic month
    age = total_days % SYNODIC_MONTH_DAYS
    return float(age)

# Entry point: lunar_age_days(dt: pendulum.DateTime) -> float

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_90txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_lunar_age_days(dt):
    result = lunar_age_days(dt)
    formatted_result = format_value_pd(result, dt)
    log_file.write(formatted_result + "\n")
