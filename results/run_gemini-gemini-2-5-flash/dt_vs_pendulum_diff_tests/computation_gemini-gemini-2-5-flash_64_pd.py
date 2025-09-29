
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def convert_time_to_minutes_since_midnight(time_24hr: pendulum.Time) -> int:
    # Step 1: Extract the hour and minute components from the pendulum.Time object
    hours = time_24hr.hour
    minutes = time_24hr.minute
    
    # Step 2: Calculate total minutes since midnight
    # Convert hours to minutes and add the existing minutes
    total_minutes = (hours * 60) + minutes
    
    # Step 3: Return the result as an integer
    return total_minutes

# Entry point: convert_time_to_minutes_since_midnight(time_24hr: pendulum.Time) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_64_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy())
def test_convert_time_to_minutes_since_midnight(time_24hr):
    result = convert_time_to_minutes_since_midnight(time_24hr)
    formatted_result = format_value_pd(result, time_24hr)
    log_file.write(formatted_result + "\n")
