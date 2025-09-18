
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timezone
def _normalize_angle_deg(angle: float) -> float:
    """
    Normalize an angle in degrees to the [0, 360) interval.
    """
    angle_mod = angle % 360.0
    # Handle potential negative modulo results explicitly (though % handles it in Python)
    if angle_mod < 0:
        angle_mod += 360.0
    return angle_mod

def _julian_date_from_datetime_utc(dt_utc: datetime) -> float:
    """
    Compute the Julian Date from a UTC datetime using the Unix epoch relation.
    JD = (seconds since 1970-01-01T00:00:00Z)/86400 + 2440587.5
    """
    # dt_utc must be timezone-aware in UTC
    unix_seconds = dt_utc.timestamp()
    jd = (unix_seconds / 86400.0) + 2440587.5
    return jd

def calculate_sidereal_time(dt: datetime, longitude_degrees: float) -> float:
    """
    Calculate the Local Sidereal Time (LST) for a given datetime and longitude.

    Inputs:
    - dt: datetime (naive treated as UTC; aware will be converted to UTC)
    - longitude_degrees: float, geographic longitude in degrees (east positive, west negative)

    Output:
    - float: Local Sidereal Time in sidereal hours within [0, 24)
    """
    # Step 1: Ensure the datetime is in UTC
    if dt.tzinfo is None:
        # Treat naive datetime as UTC by assumption
        dt_utc = dt.replace(tzinfo=timezone.utc)
    else:
        dt_utc = dt.astimezone(timezone.utc)

    # Step 2: Compute Julian Date
    jd = _julian_date_from_datetime_utc(dt_utc)

    # Step 3: Julian centuries since J2000.0
    T = (jd - 2451545.0) / 36525.0

    # Step 4: Compute GMST in degrees using IAU approximation
    gmst_deg = (
        280.46061837
        + 360.98564736629 * (jd - 2451545.0)
        + 0.000387933 * (T ** 2)
        - (T ** 3) / 38710000.0
    )
    gmst_deg = _normalize_angle_deg(gmst_deg)

    # Step 5: Local Sidereal Time in degrees (east longitudes positive)
    lst_deg = _normalize_angle_deg(gmst_deg + longitude_degrees)

    # Step 6: Convert degrees to sidereal hours
    lst_hours = lst_deg / 15.0
    if lst_hours >= 24.0:
        lst_hours -= 24.0
    elif lst_hours < 0.0:
        lst_hours += 24.0

    return lst_hours

# Entry point: calculate_sidereal_time(dt: datetime, longitude_degrees: float) -> float

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

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_93txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), float_strategy())
def test_calculate_sidereal_time(dt, longitude_degrees):
    result = calculate_sidereal_time(dt, longitude_degrees)
    formatted_result = format_value_dt(result, dt, longitude_degrees)
    log_file.write(formatted_result + "\n")
