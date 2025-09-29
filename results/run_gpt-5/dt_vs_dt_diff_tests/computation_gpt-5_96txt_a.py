
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, timedelta
import math
def equation_of_time(d: date) -> timedelta:
    """
    Calculate the Equation of Time (EoT) for a given date.

    Definition and sign:
    - EoT = apparent solar time - mean solar time.
    - A positive EoT means a sundial (apparent solar time) is ahead of a clock (mean solar time).
    
    Approximation used (Spencer/NOAA):
    EoT(minutes) = 9.87*sin(2B) - 7.53*cos(B) - 1.5*sin(B),
    where B = 2π*(n - 81)/364 and n is the day of year (1-based).

    Parameters:
    - d: datetime.date for which to compute the EoT.

    Returns:
    - datetime.timedelta representing the EoT (can be negative).
    """
    # Day of year (1..365/366)
    n = d.timetuple().tm_yday

    # Compute B in radians using the NOAA convention
    B = 2 * math.pi * (n - 81) / 364.0

    # Equation of Time in minutes (float, can be negative)
    eot_minutes = 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)

    # Convert minutes to a timedelta
    return timedelta(seconds=eot_minutes * 60.0)

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
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_96txt_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_equation_of_time(d):
    result = equation_of_time(d)
    formatted_result = format_value_dt(result, d)
    log_file.write(formatted_result + "\n")
