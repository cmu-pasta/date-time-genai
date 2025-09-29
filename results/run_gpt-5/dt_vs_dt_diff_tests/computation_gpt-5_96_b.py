
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
# Internal constants
_PI = 3.1415926535897932384626433832795028841971
_TWO_PI = 2.0 * _PI
_HALF_PI = 0.5 * _PI

def _wrap_to_pi(x: float) -> float:
    # Wrap angle to [-pi, pi]
    x = x % _TWO_PI
    if x > _PI:
        x -= _TWO_PI
    return x

def _sin_taylor(x: float) -> float:
    # Sine using Taylor series on [-pi/2, pi/2] with symmetry
    x = _wrap_to_pi(x)
    if x > _HALF_PI:
        # sin(x) = sin(pi - x)
        x = _PI - x
    elif x < -_HALF_PI:
        # sin(x) = -sin(pi + x)
        x = -(_PI + x)
    x2 = x * x
    return x * (1 - x2 / 6 + x2 * x2 / 120 - x2 * x2 * x2 / 5040)

def _cos_taylor(x: float) -> float:
    # Cosine using Taylor series on [-pi/2, pi/2] with symmetry
    x = _wrap_to_pi(x)
    sign = 1.0
    if x > _HALF_PI:
        # cos(x) = -cos(pi - x)
        x = _PI - x
        sign = -1.0
    elif x < -_HALF_PI:
        # cos(x) = -cos(pi + x)
        x = -(_PI + x)
        sign = -1.0
    x2 = x * x
    return sign * (1 - x2 / 2 + x2 * x2 / 24 - x2 * x2 * x2 / 720)

def equation_of_time_correction(d: date) -> timedelta:
    # Step 1: Compute day of year (N)
    n = (d - date(d.year, 1, 1)).days + 1

    # Step 2: Compute B in radians using NOAA's approximation: B = 2π*(N - 81)/364
    B = _TWO_PI * (n - 81) / 364.0

    # Step 3: Compute EoT in minutes: 9.87*sin(2B) - 7.53*cos(B) - 1.5*sin(B)
    eot_minutes = 9.87 * _sin_taylor(2 * B) - 7.53 * _cos_taylor(B) - 1.5 * _sin_taylor(B)

    # Step 4: Return as timedelta (positive means apparent solar time leads mean solar time)
    return timedelta(seconds=eot_minutes * 60.0)

# Entry point: equation_of_time_correction(d: date) -> timedelta

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_96_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_equation_of_time_correction(d):
    result = equation_of_time_correction(d)
    formatted_result = format_value_dt(result, d)
    log_file.write(formatted_result + "\n")
