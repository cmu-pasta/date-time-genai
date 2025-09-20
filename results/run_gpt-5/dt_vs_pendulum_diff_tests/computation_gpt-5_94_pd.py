
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def datetime_to_mjd(dt: pendulum.DateTime) -> float:
    """
    Convert a pendulum.DateTime to Modified Julian Date (MJD).
    MJD = JD - 2400000.5
    """
    # Step 1: Ensure UTC to avoid timezone-dependent shifts
    utc = dt.in_timezone("UTC")

    # Step 2: Extract date components
    Y = utc.year
    M = utc.month
    D = utc.day

    # Step 3: Compute fractional day from time components
    frac_day = (
        (utc.hour + (utc.minute + (utc.second + utc.microsecond / 1_000_000.0) / 60.0) / 60.0)
        / 24.0
    )

    # Step 4: Adjust months and years for the JD algorithm
    if M <= 2:
        Y -= 1
        M += 12

    # Step 5: Gregorian calendar correction
    A = int(Y / 100)  # floor for positive Y
    B = 2 - A + int(A / 4)

    # Step 6: Compute Julian Date (JD)
    JD = (
        int(365.25 * (Y + 4716))  # floor for positive argument
        + int(30.6001 * (M + 1))  # floor for positive argument
        + D
        + B
        - 1524.5
        + frac_day
    )

    # Step 7: Convert to Modified Julian Date
    MJD = JD - 2400000.5

    return float(MJD)

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_94_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_datetime_to_mjd(dt):
    result = datetime_to_mjd(dt)
    formatted_result = format_value_pd(result, dt)
    log_file.write(formatted_result + "\n")
