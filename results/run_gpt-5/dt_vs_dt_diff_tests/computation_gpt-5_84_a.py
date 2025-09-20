
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo
# Constants
_PI = 3.141592653589793
_TWO_PI = 2.0 * _PI
_PI_OVER_2 = _PI / 2.0

def _reduce_angle(x: float) -> float:
    # Reduce x to [-pi, pi]
    y = x % _TWO_PI
    if y > _PI:
        y -= _TWO_PI
    return y

def _sin_poly(y: float) -> float:
    # Sine Taylor polynomial up to x^9 on small |y|
    y2 = y * y
    return y * (1
                + y2 * (-1.0/6.0
                + y2 * (1.0/120.0
                + y2 * (-1.0/5040.0
                + y2 * (1.0/362880.0)))))

def _cos_poly(y: float) -> float:
    # Cosine Taylor polynomial up to x^8 on small |y|
    y2 = y * y
    return (1
            + y2 * (-1.0/2.0
            + y2 * (1.0/24.0
            + y2 * (-1.0/720.0
            + y2 * (1.0/40320.0)))))

def _sin_r(x: float) -> float:
    # Range reduce to [-pi, pi], then to [-pi/2, pi/2] via symmetry and evaluate polynomial
    y = _reduce_angle(x)
    if y > _PI_OVER_2:
        y = _PI - y
    elif y < -_PI_OVER_2:
        y = -_PI - y
    return _sin_poly(y)

def _cos_r(x: float) -> float:
    # Range reduce and apply symmetry to evaluate cosine polynomial in [-pi/2, pi/2]
    y = _reduce_angle(x)
    if y > _PI_OVER_2:
        y = _PI - y
        return -_cos_poly(y)
    if y < -_PI_OVER_2:
        y = -_PI - y
        return -_cos_poly(y)
    return _cos_poly(y)

def _arccos_via_bisection(x: float) -> float:
    # Compute arccos(x) in [0, pi] by bisection using monotonicity of cos on that interval
    if x <= -1.0:
        return _PI
    if x >= 1.0:
        return 0.0
    lo = 0.0
    hi = _PI
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        c = _cos_r(mid)
        if c > x:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)

def _day_of_year(d: date) -> int:
    # 1-based day of year
    start = date(d.year, 1, 1)
    return (d - start).days + 1

def calculate_sunset(d: date, latitude: float, longitude: float, tz: ZoneInfo) -> datetime:
    """
    Calculate the local sunset time for a given date and geographic coordinates.

    Inputs:
      - d: calendar date (naive date)
      - latitude: degrees (positive north)
      - longitude: degrees (positive east)
      - tz: ZoneInfo time zone for the output time

    Output:
      - A timezone-aware datetime representing the sunset time on date d in the given time zone.

    Notes:
      - Uses civil sunset definition (zenith 90.833 degrees).
      - Raises ValueError if the sun does not set on this date at this latitude (polar day) or does not rise (polar night).
    """
    # Step 1: Day-of-year and fractional year angle (in radians)
    N = _day_of_year(d)
    gamma = _TWO_PI / 365.0 * (N - 1)  # fractional year angle (at 12:00)

    # Step 2: Equation of Time (minutes) and Solar Declination (radians)
    sin_g = _sin_r(gamma)
    cos_g = _cos_r(gamma)
    sin_2g = _sin_r(2.0 * gamma)
    cos_2g = _cos_r(2.0 * gamma)
    sin_3g = _sin_r(3.0 * gamma)
    cos_3g = _cos_r(3.0 * gamma)

    E_minutes = 229.18 * (
        0.000075
        + 0.001868 * cos_g
        - 0.032077 * sin_g
        - 0.014615 * cos_2g
        - 0.040849 * sin_2g
    )

    decl = (
        0.006918
        - 0.399912 * cos_g
        + 0.070257 * sin_g
        - 0.006758 * cos_2g
        + 0.000907 * sin_2g
        - 0.002697 * cos_3g
        + 0.001480 * sin_3g
    )

    # Step 3: Hour angle for sunset (radians)
    zenith = (90.833 * _PI) / 180.0  # civil sunset
    lat_rad = latitude * _PI / 180.0

    sin_lat = _sin_r(lat_rad)
    cos_lat = _cos_r(lat_rad)
    cos_zen = _cos_r(zenith)

    denom = cos_lat * _cos_r(decl)
    # Avoid division by zero in extreme cases
    if abs(denom) < 1e-12:
        raise ValueError("Sunset is undefined at this latitude on the given date (denominator too small).")

    cos_omega = (cos_zen - sin_lat * _sin_r(decl)) / denom
    # Clamp numerical noise
    if cos_omega > 1.0:
        cos_omega = 1.0
    if cos_omega < -1.0:
        cos_omega = -1.0

    # If no sunset or no sunrise occurs
    if cos_omega < -1.0 + 1e-12:
        # Sun above horizon all day (no sunset)
        raise ValueError("No sunset occurs on this date at the given latitude (polar day).")
    if cos_omega > 1.0 - 1e-12:
        # Sun below horizon all day (no sunrise)
        raise ValueError("No sunset occurs on this date at the given latitude (polar night).")

    omega = _arccos_via_bisection(cos_omega)  # radians
    omega_deg = omega * 180.0 / _PI

    # Step 4: Solar noon (UTC minutes), then sunset (UTC minutes)
    solar_noon_utc_min = 720.0 - 4.0 * longitude - E_minutes
    sunset_utc_min = solar_noon_utc_min + 4.0 * omega_deg  # 4 minutes per degree

    # Step 5: Build UTC datetime and convert to local timezone
    utc_midnight = datetime(d.year, d.month, d.day, tzinfo=timezone.utc)
    sunset_dt_utc = utc_midnight + timedelta(minutes=sunset_utc_min)
    sunset_local = sunset_dt_utc.astimezone(tz)
    return sunset_local

# Entry point: calculate_sunset(d: date, latitude: float, longitude: float, tz: ZoneInfo) -> datetime

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_84_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), float_strategy(), float_strategy(), timezone_strategy())
def test_calculate_sunset(d, latitude, longitude, tz):
    result = calculate_sunset(d, latitude, longitude, tz)
    formatted_result = format_value_dt(result, d, latitude, longitude, tz)
    log_file.write(formatted_result + "\n")
