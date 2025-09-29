
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
from math import sin, cos, pi
def equation_of_time(d: date) -> timedelta:
    """
    Calculate the Equation of Time (EoT) for a given date.

    Definition:
    EoT = apparent solar time - mean solar time.
    Positive EoT means the sundial (apparent solar time) is ahead of clock time.

    Method:
    Uses the commonly employed NOAA approximation:
      B = 2π * (N - 81) / 364
      EoT_minutes = 9.87*sin(2B) - 7.53*cos(B) - 1.5*sin(B)

    Args:
        d: A calendar date (datetime.date).

    Returns:
        A datetime.timedelta representing the Equation of Time correction.
    """
    # Day of year (1..365/366)
    N = d.timetuple().tm_yday

    # Auxiliary angle in radians
    B = 2 * pi * (N - 81) / 364.0

    # Equation of Time in minutes (NOAA approximation)
    eot_minutes = 9.87 * sin(2 * B) - 7.53 * cos(B) - 1.5 * sin(B)

    # Return as a timedelta (can be positive or negative)
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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_96txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_equation_of_time(d):
    result = equation_of_time(d)
    formatted_result = format_value_dt(result, d)
    log_file.write(formatted_result + "\n")
