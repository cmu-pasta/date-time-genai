
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo
# Internal math helpers implemented without importing external libraries
def _abs(x: float) -> float:
    return -x if x < 0.0 else x

def _floor(x: float) -> int:
    # Works for positive and negative values
    i = int(x)
    return i if i <= x else i - 1

def _mod(x: float, m: float) -> float:
    # Floating-point modulo aligned with mathematical modulo
    q = _floor(x / m)
    return x - q * m

def _clamp(x: float, lo: float, hi: float) -> float:
    return lo if x < lo else (hi if x > hi else x)

# Constants
_PI = 3.141592653589793238462643383279502884
_TWO_PI = 2.0 * _PI
_HALF_PI = 0.5 * _PI
_DEG2RAD = _PI / 180.0
_RAD2DEG = 180.0 / _PI

def _sin(x: float) -> float:
    # Range reduction to [-pi, pi]
    x = _mod(x + _PI, _TWO_PI) - _PI
    # Use symmetry to reduce to [-pi/2, pi/2]
    sign = 1.0
    if x > _HALF_PI:
        x = _PI - x
        sign = 1.0
    elif x < -_HALF_PI:
        x = -_PI - x
        sign = -1.0
    # Taylor series around 0 up to x^9 term
    x2 = x * x
    term = x
    s = term
    term *= -x2 / 6.0            # -x^3/3!
    s += term
    term *= -x2 / 20.0           # +x^5/5!
    s += term
    term *= -x2 / 42.0           # -x^7/7!
    s += term
    term *= -x2 / 72.0           # +x^9/9!
    s += term
    return sign * s

def _cos(x: float) -> float:
    # cos(x) = sin(x + pi/2)
    return _sin(x + _HALF_PI)

def _tan(x: float) -> float:
    s = _sin(x)
    c = _cos(x)
    # Avoid division by very small numbers
    if _abs(c) < 1e-12:
        return 1e12 if s >= 0 else -1e12
    return s / c

def _sqrt(y: float) -> float:
    if y <= 0.0:
        return 0.0 if y == 0.0 else 0.0  # Domain not expected negative in our usage
    x = y if y >= 1.0 else 1.0
    # Newton-Raphson iterations
    for _ in range(12):
        x = 0.5 * (x + y / x)
    return x

def _atan(z: float) -> float:
    if z == 0.0:
        return 0.0
    neg = z < 0.0
    if neg:
        z = -z
    if z > 1.0:
        a = _HALF_PI - _atan(1.0 / z)
    else:
        # Taylor series up to z^9
        z2 = z * z
        a = z
        t = z * z2  # z^3
        a -= t / 3.0
        t *= z2     # z^5
        a += t / 5.0
        t *= z2     # z^7
        a -= t / 7.0
        t *= z2     # z^9
        a += t / 9.0
    return -a if neg else a

def _atan2(y: float, x: float) -> float:
    if x > 0.0:
        return _atan(y / x)
    if x < 0.0:
        return _atan(y / x) + (_PI if y >= 0.0 else -_PI)
    # x == 0
    if y > 0.0:
        return _HALF_PI
    if y < 0.0:
        return -_HALF_PI
    return 0.0

def _asin(x: float) -> float:
    x = _clamp(x, -1.0, 1.0)
    return _atan2(x, _sqrt(1.0 - x * x))

def _acos(x: float) -> float:
    x = _clamp(x, -1.0, 1.0)
    return _atan2(_sqrt(1.0 - x * x), x)

def _deg2rad(d: float) -> float:
    return d * _DEG2RAD

def _rad2deg(r: float) -> float:
    return r * _RAD2DEG

def _sin_deg(d: float) -> float:
    return _sin(_deg2rad(d))

def _cos_deg(d: float) -> float:
    return _cos(_deg2rad(d))

def _tan_deg(d: float) -> float:
    return _tan(_deg2rad(d))

def _acos_deg(x: float) -> float:
    return _rad2deg(_acos(x))

def _day_of_year(d: date) -> int:
    start = date(d.year, 1, 1)
    return (d - start).days + 1

def _normalize_deg(d: float) -> float:
    return _mod(d, 360.0)

def _normalize_hours(h: float) -> float:
    return _mod(h, 24.0)

def calculate_sunrise(d: date, latitude: float, longitude: float, tz: ZoneInfo) -> datetime:
    # NOAA Sunrise equation. Latitude positive north, longitude positive east.
    # Solar zenith for sunrise: 90°50' -> 90.833 degrees to account for refraction and solar radius.
    zenith = 90.833

    # Day of year
    N = float(_day_of_year(d))

    # Convert longitude to hour value
    lngHour = longitude / 15.0

    # Approximate time (t) in days for sunrise
    t = N + ((6.0 - lngHour) / 24.0)

    # Sun's mean anomaly
    M = (0.9856 * t) - 3.289

    # Sun's true longitude
    L = M + (1.916 * _sin_deg(M)) + (0.020 * _sin_deg(2.0 * M)) + 282.634
    L = _normalize_deg(L)

    # Right Ascension (RA)
    tanL = _tan_deg(L)
    RA = _rad2deg(_atan(tanL * 0.91764))  # atan of 0.91764 * tan(L)
    RA = _normalize_deg(RA)

    # Quadrant adjustment
    L_quadrant = _floor(L / 90.0) * 90.0
    RA_quadrant = _floor(RA / 90.0) * 90.0
    RA = RA + (L_quadrant - RA_quadrant)

    # Convert RA to hours
    RA_hours = RA / 15.0

    # Sun's declination
    sinDec = 0.39782 * _sin_deg(L)
    cosDec = _sqrt(1.0 - sinDec * sinDec)

    # Local hour angle
    cosH_numer = _cos_deg(zenith) - (sinDec * _sin_deg(latitude))
    cosH_denom = cosDec * _cos_deg(latitude)
    # Avoid division by zero
    if _abs(cosH_denom) < 1e-12:
        raise ValueError("Computation unstable at this latitude.")
    cosH = cosH_numer / cosH_denom

    # Check for polar day/night conditions
    if cosH > 1.0:
        raise ValueError("Sun never rises on this date at the given location.")
    if cosH < -1.0:
        raise ValueError("Sun never sets on this date at the given location; no distinct sunrise.")

    # Local hour angle for sunrise
    H = 360.0 - _acos_deg(_clamp(cosH, -1.0, 1.0))
    H_hours = H / 15.0

    # Local mean time of rising
    T = H_hours + RA_hours - (0.06571 * t) - 6.622

    # Adjust to UTC
    UT = _normalize_hours(T - lngHour)

    # Build timezone-aware datetime
    # Convert UT hours to time components
    hour = int(UT)
    minute_float = (UT - hour) * 60.0
    minute = int(minute_float)
    second = int((minute_float - minute) * 60.0 + 0.5)

    # Normalize seconds/minutes overflow
    carry_min = 0
    if second >= 60:
        second -= 60
        carry_min = 1
    minute += carry_min
    carry_hour = 0
    if minute >= 60:
        minute -= 60
        carry_hour = 1
    hour = (hour + carry_hour) % 24

    # Construct UTC datetime on the given date
    dt_utc = datetime(d.year, d.month, d.day, hour, minute, second, tzinfo=timezone.utc)

    # Convert to target timezone
    dt_local = dt_utc.astimezone(tz)

    return dt_local

# Entry point: calculate_sunrise(d: date, latitude: float, longitude: float, tz: ZoneInfo) -> datetime

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_78_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), float_strategy(), float_strategy(), timezone_strategy())
def test_calculate_sunrise(d, latitude, longitude, tz):
    result = calculate_sunrise(d, latitude, longitude, tz)
    formatted_result = format_value_dt(result, d, latitude, longitude, tz)
    log_file.write(formatted_result + "\n")
