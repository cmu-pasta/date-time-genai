
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def days_since_reference(target_dt: pendulum.DateTime, reference_dt: pendulum.DateTime) -> int:
    # Step 1: Calculate the duration between the target date and the reference date.
    # The diff() method returns a pendulum.Duration object.
    duration = target_dt.diff(reference_dt)
    
    # Step 2: Extract the total number of days from the duration.
    # in_days() returns an integer representing the total number of days,
    # including negative values if target_dt is before reference_dt.
    days_count = duration.in_days()
    
    # Step 3: Return the result as an integer.
    return days_count

# Entry point: days_since_reference(target_dt: pendulum.DateTime, reference_dt: pendulum.DateTime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_76_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy(), datetime_strategy())
def test_days_since_reference(target_dt, reference_dt):
    result = days_since_reference(target_dt, reference_dt)
    formatted_result = format_value_pd(result, target_dt, reference_dt)
    log_file.write(formatted_result + "\n")
