
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import math
import pendulum
def calculate_equation_of_time(date: pendulum.Date) -> pendulum.Duration:
    """
    Calculate the Equation of Time (EoT) for a given date.

    The EoT is the discrepancy (apparent solar time - mean solar time),
    approximated in minutes by:
        EoT ≈ 9.87*sin(2B) - 7.53*cos(B) - 1.5*sin(B)
    where B = 2π*(N - 81)/364 and N is the day-of-year (1..366).

    Args:
        date: pendulum.Date representing the date for which to compute the EoT.

    Returns:
        pendulum.Duration representing the EoT (can be negative).
    """
    # Day of year (N)
    N = date.day_of_year

    # Auxiliary angle B in radians
    B = (2 * math.pi) * (N - 81) / 364.0

    # Equation of Time in minutes (approximation)
    eot_minutes = 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)

    # Convert to a pendulum.Duration (allowing negative durations)
    eot_seconds = eot_minutes * 60.0
    return pendulum.duration(seconds=eot_seconds)

# Entry point: calculate_equation_of_time(date: pendulum.Date) -> pendulum.Duration

def format_value_pd(*values):
    formatted_values = []

    for value in values:
        if isinstance(value, pendulum.DateTime):
            formatted_values.append(value.to_iso8601_string()[:-1])
        elif isinstance(value, pendulum.Date):
            formatted_values.append(value.to_date_string())
        elif isinstance(value, pendulum.Time):
            # Format time in the same way as datetime.time.isoformat() does
            formatted_time = (
                str(value.hour).zfill(2)
                + ":"
                + str(value.minute).zfill(2)
                + ":"
                + str(value.second).zfill(2)
            )
            if value.microsecond:
                # Padding microseconds to 6 digits
                formatted_time += "." + str(value.microsecond).zfill(6)
            formatted_values.append(formatted_time)
        elif isinstance(value, pendulum.Duration):
            formatted_values.append(str(value.total_seconds()))
        else:
            formatted_values.append(str(value))

    return ", ".join(formatted_values)

if not os.path.exists(".logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs(".logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_96txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_calculate_equation_of_time(date):
    result = calculate_equation_of_time(date)
    formatted_result = format_value_pd(result, date)
    log_file.write(formatted_result + "\n")
