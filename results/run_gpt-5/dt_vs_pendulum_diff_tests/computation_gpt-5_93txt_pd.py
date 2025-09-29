
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def _normalize_degrees(deg: float) -> float:
    # Normalize angle to [0, 360)
    result = deg % 360.0
    if result < 0.0:
        result += 360.0
    return result

def _julian_date(dt_utc: pendulum.DateTime) -> float:
    # Compute Julian Date from a UTC datetime
    y = dt_utc.year
    m = dt_utc.month
    D = dt_utc.day
    # Fractional day
    frac_day = (dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0 + dt_utc.microsecond / 3_600_000_000.0) / 24.0

    if m <= 2:
        y -= 1
        m += 12

    A = int(y // 100)
    B = 2 - A + int(A // 4)

    jd = int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + D + B - 1524.5 + frac_day
    return float(jd)

def calculate_sidereal_time(dt: pendulum.DateTime, longitude_degrees: float) -> pendulum.Time:
    """
    Calculate the local sidereal time for a given datetime and longitude.

    Inputs:
    - dt: pendulum.DateTime (any timezone; will be converted to UTC internally)
    - longitude_degrees: float (east-positive, in degrees)

    Output:
    - pendulum.Time representing the local sidereal time (LST)
    """
    # Step 1: Ensure UTC
    dt_utc = dt.in_timezone("UTC")

    # Step 2: Julian Date
    JD = _julian_date(dt_utc)

    # Step 3: Centuries since J2000.0
    T = (JD - 2451545.0) / 36525.0

    # Step 4: GMST in degrees (IAU 1982/2000-era approximation)
    GMST_deg = 280.46061837 + 360.98564736629 * (JD - 2451545.0) + 0.000387933 * (T * T) - (T * T * T) / 38710000.0
    GMST_deg = _normalize_degrees(GMST_deg)

    # Step 5: Local Sidereal Time in degrees
    LST_deg = _normalize_degrees(GMST_deg + longitude_degrees)

    # Step 6: Convert degrees to time-of-day
    total_sidereal_hours = LST_deg / 15.0  # 360 deg == 24 hours
    hours = int(total_sidereal_hours)
    rem_h = (total_sidereal_hours - hours) * 60.0
    minutes = int(rem_h)
    rem_m = (rem_h - minutes) * 60.0
    seconds = int(rem_m)
    rem_s = (rem_m - seconds)
    microseconds = int(round(rem_s * 1_000_000.0))

    # Handle rounding overflow
    if microseconds >= 1_000_000:
        microseconds -= 1_000_000
        seconds += 1
    if seconds >= 60:
        seconds -= 60
        minutes += 1
    if minutes >= 60:
        minutes -= 60
        hours += 1
    if hours >= 24:
        hours -= 24

    # Step 7: Return pendulum.Time
    return pendulum.Time(hours, minutes, seconds, microseconds)

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

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_93txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), float_strategy())
def test_calculate_sidereal_time(dt, longitude_degrees):
    result = calculate_sidereal_time(dt, longitude_degrees)
    formatted_result = format_value_pd(result, dt, longitude_degrees)
    log_file.write(formatted_result + "\n")
