
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def determine_season(dt: pendulum.DateTime) -> int:
    """
    Determine the meteorological season (Northern Hemisphere) for a given date.

    Season codes:
      1 -> Spring  (Mar-May)
      2 -> Summer  (Jun-Aug)
      3 -> Autumn  (Sep-Nov)
      4 -> Winter  (Dec-Feb)

    Parameters:
      dt (pendulum.DateTime): The date/time to evaluate.

    Returns:
      int: The season code as defined above.
    """
    month = dt.month
    if 3 <= month <= 5:
        return 1  # Spring
    elif 6 <= month <= 8:
        return 2  # Summer
    elif 9 <= month <= 11:
        return 3  # Autumn
    else:
        return 4  # Winter

# Entry point: determine_season(dt: pendulum.DateTime) -> int

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_19txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_determine_season(dt):
    result = determine_season(dt)
    formatted_result = format_value_pd(result, dt)
    log_file.write(formatted_result + "\n")
