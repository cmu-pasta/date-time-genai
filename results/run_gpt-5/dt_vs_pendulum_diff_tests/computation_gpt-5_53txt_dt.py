
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, datetime, timedelta, timezone
import math
def _julian_day_from_datetime(dt: datetime) -> float:
    """
    Convert a timezone-aware UTC datetime to Julian Day (UTC-based).
    """
    if dt.tzinfo is None:
        # Assume UTC if naive
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    unix_epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    days_since_epoch = (dt - unix_epoch).total_seconds() / 86400.0
    return 2440587.5 + days_since_epoch

def _normalize_deg(x: float) -> float:
    """Normalize angle to [0, 360) degrees."""
    return x % 360.0

def _normalize_deg180(x: float) -> float:
    """Normalize angle to (-180, 180] degrees."""
    return ((x + 180.0) % 360.0) - 180.0

def _solar_ecliptic_longitude_deg(dt: datetime) -> float:
    """
    Approximate apparent ecliptic longitude of the Sun (degrees) for a given UTC datetime.
    Uses a low-accuracy formula sufficient to locate equinox date.
    """
    JD = _julian_day_from_datetime(dt)
    n = JD - 2451545.0  # days since J2000.0
    # Mean longitude and anomaly (degrees)
    L = 280.460 + 0.9856474 * n
    g = 357.528 + 0.9856003 * n
    # Convert to radians for trig
    g_rad = math.radians(g)
    # Approximate ecliptic longitude (degrees)
    lam = L + 1.915 * math.sin(g_rad) + 0.020 * math.sin(2.0 * g_rad)
    return _normalize_deg(lam)

def _find_bracketing_interval(year: int) -> tuple:
    """
    Find a 1-day interval in UTC around the September equinox for the given year
    where the function crosses zero: f(t) = normalized(lambda(t)-180).
    Returns a tuple (start_datetime, end_datetime) in UTC.
    """
    # Start with a reasonable search window around late September
    start_day = datetime(year, 9, 15, 0, 0, tzinfo=timezone.utc)
    end_day = datetime(year, 9, 28, 0, 0, tzinfo=timezone.utc)

    def f(dt: datetime) -> float:
        return _normalize_deg180(_solar_ecliptic_longitude_deg(dt) - 180.0)

    # Step through days to find a sign change
    t = start_day
    prev_val = f(t)
    while t < end_day:
        t_next = t + timedelta(days=1)
        next_val = f(t_next)
        # Check for sign change or exact zero
        if prev_val == 0.0:
            return (t, t_next)
        if next_val == 0.0:
            return (t, t_next)
        if prev_val * next_val < 0.0:
            return (t, t_next)
        t = t_next
        prev_val = next_val

    # If not found, expand the search window (rare, for extreme years)
    start_day = datetime(year, 8, 15, 0, 0, tzinfo=timezone.utc)
    end_day = datetime(year, 10, 31, 0, 0, tzinfo=timezone.utc)
    t = start_day
    prev_val = f(t)
    while t < end_day:
        t_next = t + timedelta(days=1)
        next_val = f(t_next)
        if prev_val == 0.0 or next_val == 0.0 or (prev_val * next_val < 0.0):
            return (t, t_next)
        t = t_next
        prev_val = next_val

    # As a fallback, return a default narrow window around Sep 22-23
    return (datetime(year, 9, 22, 0, 0, tzinfo=timezone.utc),
            datetime(year, 9, 23, 0, 0, tzinfo=timezone.utc))

def _bisection_zero_crossing(start_dt: datetime, end_dt: datetime) -> datetime:
    """
    Refine the time of the zero crossing of f(t) = normalized(lambda(t)-180)
    within [start_dt, end_dt] using bisection. Returns a UTC datetime.
    """
    def f(dt: datetime) -> float:
        return _normalize_deg180(_solar_ecliptic_longitude_deg(dt) - 180.0)

    a = start_dt
    b = end_dt
    fa = f(a)
    fb = f(b)

    # If endpoints are exactly zero, return that
    if fa == 0.0:
        return a
    if fb == 0.0:
        return b

    # Ensure there is a sign change; if not, still try to refine
    for _ in range(60):  # ~1e-18 fraction of day if perfectly bracketed; we will stop earlier by resolution
        mid = a + (b - a) / 2
        fm = f(mid)

        # Stop when interval is below 1 second
        if (b - a).total_seconds() <= 1.0:
            return mid

        # Standard bisection step; prefer bracketing sign change
        if fa == 0.0:
            return a
        if fb == 0.0:
            return b
        if fa * fm <= 0.0:
            b, fb = mid, fm
        else:
            a, fa = mid, fm

    return a + (b - a) / 2

def autumnal_equinox_date(year: int) -> date:
    """
    Compute the UTC calendar date of the autumnal equinox (September equinox) for the given year.
    Returns a date object representing the UTC date on which the equinox occurs.
    """
    # Find a daily interval that brackets the equinox crossing
    start_dt, end_dt = _find_bracketing_interval(year)
    # Refine to precise crossing time (UTC)
    equinox_dt = _bisection_zero_crossing(start_dt, end_dt)
    # Return the UTC date
    return equinox_dt.date()

# Entry point: autumnal_equinox_date(year: int) -> date

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_53txt_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_autumnal_equinox_date(year):
    result = autumnal_equinox_date(year)
    formatted_result = format_value_dt(result, year)
    log_file.write(formatted_result + "\n")
