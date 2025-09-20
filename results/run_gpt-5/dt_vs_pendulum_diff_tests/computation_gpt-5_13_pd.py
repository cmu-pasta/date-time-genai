
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def determine_quarter(dt: pendulum.DateTime) -> int:
    """
    Determine the quarter of the year for the given pendulum.DateTime.
    
    Args:
        dt (pendulum.DateTime): The date-time for which to determine the quarter.
    
    Returns:
        int: The quarter number (1 to 4).
    """
    return dt.quarter

# Entry point: determine_quarter(dt: pendulum.DateTime) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_13_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_determine_quarter(dt):
    result = determine_quarter(dt)
    formatted_result = format_value_pd(result, dt)
    log_file.write(formatted_result + "\n")
