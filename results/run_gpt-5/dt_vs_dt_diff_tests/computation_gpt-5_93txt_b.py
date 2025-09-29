
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timezone
def _normalize_degrees(angle: float) -> float:
    """
    Normalize an angle in degrees to the range [0, 360).
    """
    return angle % 360.0

def _julian_date(dt_utc: datetime) -> float:
    """
    Convert a UTC datetime (naive, assumed UTC) to Julian Date (JD).
    Uses the proleptic Gregorian calendar for all dates.
    """
    year = dt_utc.year
    month = dt_utc.month
    day = dt_utc.day
    hour = dt_utc.hour
    minute = dt_utc.minute
    second = dt_utc.second
    microsecond = dt_utc.microsecond

    # Integer Julian Day Number (JDN)
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    jdn = day + ((153 * m + 2) // 5) + 365 * y + y // 4 - y // 100 + y // 400 - 32045

    # Fractional day (JD starts at noon UTC)
    frac_day = ((hour - 12) / 24.0) + (minute / 1440.0) + (second / 86400.0) + (microsecond / 86400_000000.0)

    return jdn + frac_day

def calculate_local_sidereal_time_degrees(dt: datetime, longitude_degrees: float) -> float:
    """
    Calculate the Local Sidereal Time (LST) in degrees for a given datetime and longitude.

    Inputs:
    - dt: datetime. If timezone-aware, it will be converted to UTC. If naive, it is assumed to be UTC.
    - longitude_degrees: float. Observer's longitude in degrees (east positive, west negative).

    Output:
    - float: Local Sidereal Time in degrees in the range [0.0, 360.0).
    """
    # Step 1: Normalize datetime to UTC (naive treated as UTC)
    if dt.tzinfo is not None:
        dt_utc = dt.astimezone(timezone.utc).replace(tzinfo=None)
    else:
        dt_utc = dt

    # Step 2: Convert to Julian Date
    jd = _julian_date(dt_utc)

    # Step 3: Centuries since J2000.0
    T = (jd - 2451545.0) / 36525.0

    # Step 4: Compute GMST in degrees (IAU 2006-compatible approximation)
    # GMST = 280.46061837 + 360.98564736629*(JD - 2451545.0) + 0.000387933*T^2 - (T^3)/38710000
    gmst_deg = (
        280.46061837
        + 360.98564736629 * (jd - 2451545.0)
        + 0.000387933 * (T * T)
        - (T * T * T) / 38710000.0
    )
    gmst_deg = _normalize_degrees(gmst_deg)

    # Step 5: Local Sidereal Time = GMST + longitude (east-positive)
    lst_deg = _normalize_degrees(gmst_deg + longitude_degrees)

    # Step 6: Return LST in degrees
    return lst_deg

# Entry point: calculate_local_sidereal_time_degrees(dt: datetime, longitude_degrees: float) -> float

def format_value_dt(*values):
    formatted_values = []

    for value in values:
        if isinstance(value, datetime):
            formatted_values.append(value.isoformat())
        elif isinstance(value, date):
            # Use strftime to format the date similar to to_date_string()
            formatted_values.append(value.strftime("%Y-%m-%d"))
        elif isinstance(value, time):
            formatted_values.append(value.isoformat())
        elif isinstance(value, timedelta):
            formatted_values.append(str(value.total_seconds()))
        else:
            formatted_values.append(str(value))

    return ", ".join(formatted_values)

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_93txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), float_strategy())
def test_calculate_local_sidereal_time_degrees(dt, longitude_degrees):
    result = calculate_local_sidereal_time_degrees(dt, longitude_degrees)
    formatted_result = format_value_dt(result, dt, longitude_degrees)
    log_file.write(formatted_result + "\n")
