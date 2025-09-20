
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, timezone, time
def _to_utc(dt: datetime) -> datetime:
    # Convert to UTC; if naive, assume it's already UTC
    if dt.tzinfo is not None:
        return dt.astimezone(timezone.utc)
    return dt

def _julian_date(dt_utc: datetime) -> float:
    # Compute Julian Date for a UTC datetime (including fractional day)
    year = dt_utc.year
    month = dt_utc.month
    day = dt_utc.day

    hour = dt_utc.hour
    minute = dt_utc.minute
    second = dt_utc.second
    microsecond = dt_utc.microsecond

    # Fractional day
    day_fraction = (
        (hour / 24.0)
        + (minute / 1440.0)
        + ((second + microsecond / 1_000_000.0) / 86400.0)
    )

    # Shift months so that March = 3 ... January = 13, February = 14 of previous year
    if month <= 2:
        year_adj = year - 1
        month_adj = month + 12
    else:
        year_adj = year
        month_adj = month

    A = int(year_adj / 100)
    B = 2 - A + int(A / 4)

    # Note: int(x) truncates toward zero; here all terms are positive, so it acts as floor
    jd_integer = (
        int(365.25 * (year_adj + 4716))
        + int(30.6001 * (month_adj + 1))
        + day
        + B
        - 1524
    )

    # The standard JD uses .5 offset to begin days at noon UT
    JD = jd_integer - 0.5 + day_fraction
    return JD

def calculate_sidereal_time(dt: datetime, longitude_degrees: float) -> time:
    """
    Calculate Local Sidereal Time for the given datetime and longitude.
    - dt: datetime (timezone-aware will be converted to UTC; naive assumed UTC)
    - longitude_degrees: float (east positive, west negative)
    Returns: datetime.time representing LST (in sidereal hours/minutes/seconds)
    """
    dt_utc = _to_utc(dt)
    JD = _julian_date(dt_utc)
    D = JD - 2451545.0  # Days since J2000.0

    # GMST in hours (approximation suitable for many applications)
    GMST_hours = 18.697374558 + 24.06570982441908 * D

    # Local Sidereal Time (in hours), longitude east positive
    LST_hours = GMST_hours + (longitude_degrees / 15.0)

    # Normalize to [0, 24)
    LST_hours = LST_hours % 24.0

    # Convert fractional hours to time components
    h = int(LST_hours)
    rem_min = (LST_hours - h) * 60.0
    m = int(rem_min)
    rem_sec = (rem_min - m) * 60.0
    s = int(rem_sec)
    us = int(round((rem_sec - s) * 1_000_000))

    # Handle rounding overflow (e.g., 59.999999 -> 60.000000)
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

    return time(hour=h, minute=m, second=s, microsecond=us)

# Entry point: calculate_sidereal_time(dt: datetime, longitude_degrees: float) -> time

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_93_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), float_strategy())
def test_calculate_sidereal_time(dt, longitude_degrees):
    result = calculate_sidereal_time(dt, longitude_degrees)
    formatted_result = format_value_dt(result, dt, longitude_degrees)
    log_file.write(formatted_result + "\n")
