
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import math
import pendulum
def calculate_sidereal_time(dt: pendulum.DateTime, longitude_degrees: float) -> pendulum.Time:
    # Ensure we are working in UTC for astronomical time calculations
    utc_dt = dt.in_timezone(pendulum.timezone("UTC"))

    # Extract date-time components
    year = utc_dt.year
    month = utc_dt.month
    day = utc_dt.day
    hour = utc_dt.hour
    minute = utc_dt.minute
    second = utc_dt.second
    microsecond = utc_dt.microsecond

    # Convert to Julian Date (JD) with fractional day
    # Algorithm accounts for Gregorian calendar
    Y = year
    M = month
    D = float(day) + (hour + (minute + (second + microsecond / 1_000_000.0) / 60.0) / 60.0) / 24.0
    if M <= 2:
        Y -= 1
        M += 12
    A = math.floor(Y / 100)
    B = 2 - A + math.floor(A / 4)
    JD = math.floor(365.25 * (Y + 4716)) + math.floor(30.6001 * (M + 1)) + D + B - 1524.5

    # JD at 0h UT (start of the current UTC day)
    JD0 = math.floor(JD + 0.5) - 0.5

    # Hours since 0h UT
    H = (JD - JD0) * 24.0

    # Days since J2000.0 and centuries for precision term
    D_since_J2000 = JD - 2451545.0
    D0_since_J2000 = JD0 - 2451545.0
    T = D_since_J2000 / 36525.0

    # Compute GMST in hours using a standard approximation (Vallado)
    GMST_hours = (
        6.697374558
        + 0.06570982441908 * D0_since_J2000
        + 1.00273790935 * H
        + 0.000026 * (T * T)
    )

    # Normalize GMST to [0, 24)
    GMST_hours = GMST_hours % 24.0

    # Convert longitude from degrees to hours and compute Local Sidereal Time
    longitude_hours = longitude_degrees / 15.0
    LST_hours = (GMST_hours + longitude_hours) % 24.0

    # Convert fractional hours to h:m:s.us for pendulum.Time
    h = int(math.floor(LST_hours))
    rem_min = (LST_hours - h) * 60.0
    m = int(math.floor(rem_min))
    rem_sec = (rem_min - m) * 60.0
    s = int(math.floor(rem_sec))
    us = int(round((rem_sec - s) * 1_000_000.0))

    # Handle possible rounding overflow
    if us >= 1_000_000:
        us -= 1_000_000
        s += 1
    if s >= 60:
        s -= 60
        m += 1
    if m >= 60:
        m -= 60
        h += 1
    if h >= 24:
        h -= 24

    # Return as pendulum.Time (UTC-neutral, as LST is a local sidereal angle)
    return pendulum.time(hour=h, minute=m, second=s, microsecond=us)

# Entry point: calculate_sidereal_time(dt: pendulum.DateTime, longitude_degrees: float) -> pendulum.Time

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_93_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), float_strategy())
def test_calculate_sidereal_time(dt, longitude_degrees):
    result = calculate_sidereal_time(dt, longitude_degrees)
    formatted_result = format_value_pd(result, dt, longitude_degrees)
    log_file.write(formatted_result + "\n")
