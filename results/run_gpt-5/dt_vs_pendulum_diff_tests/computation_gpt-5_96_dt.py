
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
def _wrap_to_pi(x: float) -> float:
    # Reduce angle to [-pi, pi] to improve series accuracy
    pi = 3.141592653589793
    two_pi = 2.0 * pi
    # Python's modulo handles floats; ensure value is in [-pi, pi]
    y = (x + pi) % two_pi
    if y < 0.0:
        y += two_pi
    return y - pi

def _sin(x: float) -> float:
    # Sine via Taylor series around 0 with argument reduction
    x = _wrap_to_pi(x)
    x2 = x * x
    # x - x^3/3! + x^5/5! - x^7/7! + x^9/9!
    return x * (
        1.0
        - x2 / 6.0
        + x2 * x2 / 120.0
        - x2 * x2 * x2 / 5040.0
        + x2 * x2 * x2 * x2 / 362880.0
    )

def _cos(x: float) -> float:
    # Cosine via Taylor series around 0 with argument reduction
    x = _wrap_to_pi(x)
    x2 = x * x
    # 1 - x^2/2! + x^4/4! - x^6/6! + x^8/8!
    return (
        1.0
        - x2 / 2.0
        + x2 * x2 / 24.0
        - x2 * x2 * x2 / 720.0
        + x2 * x2 * x2 * x2 / 40320.0
    )

def equation_of_time(d: date) -> timedelta:
    """
    Compute the equation of time for a given date.
    Returns the correction as a timedelta (positive means apparent sun is ahead).
    """
    # Day of year N (1..366)
    N = d.timetuple().tm_yday

    # Compute B in radians: B = 2π*(N - 81)/364 (NOAA approximation)
    pi = 3.141592653589793
    B = 2.0 * pi * (N - 81.0) / 364.0

    # Equation of time in minutes
    eot_minutes = 9.87 * _sin(2.0 * B) - 7.53 * _cos(B) - 1.5 * _sin(B)

    # Return as timedelta
    return timedelta(minutes=eot_minutes)

# Entry point: equation_of_time(d: date) -> timedelta

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_96_dt.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_equation_of_time(d):
    result = equation_of_time(d)
    formatted_result = format_value_dt(result, d)
    log_file.write(formatted_result + "\n")
