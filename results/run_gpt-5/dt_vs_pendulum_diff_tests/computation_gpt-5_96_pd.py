
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
import math
def equation_of_time_minutes(date: pendulum.Date) -> float:
    """
    Calculate the Equation of Time (EoT) for a given date.

    Parameters:
        date (pendulum.Date): The date for which to compute the EoT.

    Returns:
        float: The Equation of Time in minutes. Positive values indicate
               apparent solar time is ahead of mean solar time.
    """
    # Step 1: Extract the day of year using Pendulum
    n = date.day_of_year

    # Step 2: Compute the auxiliary angle B (in radians)
    B = 2.0 * math.pi * (n - 81.0) / 364.0

    # Step 3: Compute the Equation of Time in minutes (NOAA approximation)
    eot_minutes = 9.87 * math.sin(2.0 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)

    # Step 4: Return the result as a float (minutes)
    return float(eot_minutes)

# Entry point: equation_of_time_minutes(date: pendulum.Date) -> float

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_96_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_equation_of_time_minutes(date):
    result = equation_of_time_minutes(date)
    formatted_result = format_value_pd(result, date)
    log_file.write(formatted_result + "\n")
