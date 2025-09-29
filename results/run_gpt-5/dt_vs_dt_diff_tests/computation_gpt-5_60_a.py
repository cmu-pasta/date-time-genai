
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import datetime, date as Date, timedelta, timezone
from zoneinfo import ZoneInfo
def _normalize_angle(x: float) -> float:
    # Normalize angle to [-pi, pi] for better series convergence
    pi = 3.141592653589793
    two_pi = 2.0 * pi
    y = x % two_pi
    if y > pi:
        y -= two_pi
    return y

def _sin(x: float) -> float:
    # Sine via Taylor series with angle reduction
    x = _normalize_angle(x)
    term = x
    s = x
    # Add terms up to x^11/11! for reasonable accuracy
    # term_k = term_{k-1} * (-x^2) / ((2k)*(2k+1))
    x2 = x * x
    for k in range(1, 6):
        term *= -x2 / ( (2.0 * k) * (2.0 * k + 1.0) )
        s += term
    return s

def _cos(x: float) -> float:
    # Cosine via Taylor series with angle reduction
    x = _normalize_angle(x)
    term = 1.0
    s = 1.0
    x2 = x * x
    # term_k = term_{k-1} * (-x^2) / ((2k-1)*(2k))
    for k in range(1, 7):
        term *= -x2 / ( (2.0 * k - 1.0) * (2.0 * k) )
        s += term
    return s

def calculate_solar_noon(given_date: Date, latitude_degrees: float, longitude_degrees: float, tz: ZoneInfo) -> datetime:
    # Step 1: Day of year
    N = given_date.timetuple().tm_yday

    # Step 2: Fractional year gamma (radians) at local mean solar noon approximation
    pi = 3.141592653589793
    gamma = (2.0 * pi / 365.0) * (N - 1.0)

    # Step 3: Equation of Time (minutes) using NOAA approximation
    E = 229.18 * (
        0.000075
        + 0.001868 * _cos(gamma)
        - 0.032077 * _sin(gamma)
        - 0.014615 * _cos(2.0 * gamma)
        - 0.040849 * _sin(2.0 * gamma)
    )

    # Step 4: Solar noon time in UTC minutes from 00:00 UTC
    # Convention: longitude east positive, west negative
    solar_noon_utc_minutes = 720.0 - 4.0 * longitude_degrees - E

    # Step 5: Construct UTC datetime for given date and add the computed minutes
    utc_midnight = datetime(given_date.year, given_date.month, given_date.day, tzinfo=timezone.utc)
    solar_noon_utc_dt = utc_midnight + timedelta(minutes=solar_noon_utc_minutes)

    # Step 6: Convert to local timezone and return
    solar_noon_local = solar_noon_utc_dt.astimezone(tz)
    return solar_noon_local

# Entry point: calculate_solar_noon(given_date: date, latitude_degrees: float, longitude_degrees: float, tz: ZoneInfo) -> datetime

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_60_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), float_strategy(), float_strategy(), timezone_strategy())
def test_calculate_solar_noon(given_date, latitude_degrees, longitude_degrees, tz):
    result = calculate_solar_noon(given_date, latitude_degrees, longitude_degrees, tz)
    formatted_result = format_value_dt(result, given_date, latitude_degrees, longitude_degrees, tz)
    log_file.write(formatted_result + "\n")
