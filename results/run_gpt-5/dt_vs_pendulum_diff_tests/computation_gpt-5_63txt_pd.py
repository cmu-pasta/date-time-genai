
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_fortnights_between(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> int:
    """
    Calculate the number of complete fortnights (14-day periods) between two Pendulum DateTime objects.
    
    Args:
        dt1: A pendulum.DateTime object representing the first date/time.
        dt2: A pendulum.DateTime object representing the second date/time.
    
    Returns:
        An integer representing the absolute number of complete fortnights between dt1 and dt2.
    """
    # Step 1: Compute absolute difference in days
    days_difference: int = abs(dt2.diff(dt1).in_days())
    
    # Step 2: Convert days to complete fortnights (14-day periods)
    fortnights: int = days_difference // 14
    
    # Step 3: Return the number of fortnights as an integer
    return fortnights

# Entry point: calculate_fortnights_between(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> int

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_63txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_calculate_fortnights_between(dt1, dt2):
    result = calculate_fortnights_between(dt1, dt2)
    formatted_result = format_value_pd(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
