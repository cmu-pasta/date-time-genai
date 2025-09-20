
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_middle_date(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> pendulum.DateTime:
    # Step 1: Calculate the total duration between the two dates
    # Subtracting two DateTime objects results in a pendulum.Duration object
    total_duration = dt2 - dt1
    
    # Step 2: Calculate half of the total duration
    half_duration = total_duration / 2
    
    # Step 3: Add the half duration to the first date to find the middle date.
    # This works correctly even if dt1 is chronologically after dt2,
    # as half_duration will be negative in that case.
    middle_date = dt1 + half_duration
    
    # Step 4: Return the resulting middle date
    return middle_date

# Entry point: find_middle_date(dt1: pendulum.DateTime, dt2: pendulum.DateTime) -> pendulum.DateTime

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_32_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_find_middle_date(dt1, dt2):
    result = find_middle_date(dt1, dt2)
    formatted_result = format_value_pd(result, dt1, dt2)
    log_file.write(formatted_result + "\n")
