
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_hours_difference(t1: pendulum.Time, t2: pendulum.Time) -> float:
    # Step 1: Calculate the difference between the two pendulum.Time objects.
    # Subtracting two pendulum.Time objects results in a pendulum.Duration.
    duration = t2 - t1
    
    # Step 2: Get the total number of hours from the duration as a float.
    # The .total_hours property gives the difference including fractional hours.
    hours_difference = duration.total_hours
    
    # Step 3: Return the absolute value of the difference to ensure a positive result.
    return abs(hours_difference)

# Entry point: calculate_hours_difference(t1: pendulum.Time, t2: pendulum.Time) -> float

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_18_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy(), time_strategy())
def test_calculate_hours_difference(t1, t2):
    result = calculate_hours_difference(t1, t2)
    formatted_result = format_value_pd(result, t1, t2)
    log_file.write(formatted_result + "\n")
