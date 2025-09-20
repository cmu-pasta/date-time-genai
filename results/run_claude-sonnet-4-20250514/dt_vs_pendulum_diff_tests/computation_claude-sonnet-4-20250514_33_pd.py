
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_minutes_between_times(time1: pendulum.Time, time2: pendulum.Time) -> int:
    # Step 1: Get a reference date (today) to convert times to datetime objects
    today = pendulum.today()
    
    # Step 2: Convert Time objects to DateTime objects on the same day
    dt1 = today.replace(hour=time1.hour, minute=time1.minute, second=time1.second, microsecond=time1.microsecond)
    dt2 = today.replace(hour=time2.hour, minute=time2.minute, second=time2.second, microsecond=time2.microsecond)
    
    # Step 3: Calculate the difference in minutes
    difference = abs(dt2.diff(dt1).in_minutes())
    
    # Step 4: Return the result as an integer
    return difference

# Entry point: calculate_minutes_between_times(time1: pendulum.Time, time2: pendulum.Time) -> int

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_33_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy(), time_strategy())
def test_calculate_minutes_between_times(time1, time2):
    result = calculate_minutes_between_times(time1, time2)
    formatted_result = format_value_pd(result, time1, time2)
    log_file.write(formatted_result + "\n")
