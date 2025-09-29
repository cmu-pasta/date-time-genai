
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_year_progress(dt: pendulum.DateTime) -> float:
    # Step 1: Determine the start and end of the year for the given datetime
    start_of_year = dt.start_of('year')
    end_of_year = dt.end_of('year')
    
    # Step 2: Compute durations using pendulum.Duration via datetime subtraction
    elapsed_duration = dt - start_of_year
    total_duration = end_of_year - start_of_year

    # Step 3: Convert durations to microseconds for maximum precision
    elapsed_us = elapsed_duration.in_microseconds()
    total_us = total_duration.in_microseconds()

    # Step 4: Clamp elapsed to [0, total] to handle out-of-year inputs robustly
    if elapsed_us < 0:
        elapsed_us = 0
    if elapsed_us > total_us:
        elapsed_us = total_us

    # Step 5: Compute percentage of the year that has passed
    percentage = (elapsed_us / total_us) * 100.0 if total_us > 0 else 0.0
    return float(percentage)

# Entry point: calculate_year_progress(dt: pendulum.DateTime) -> float

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_54txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_year_progress(dt):
    result = calculate_year_progress(dt)
    formatted_result = format_value_pd(result, dt)
    log_file.write(formatted_result + "\n")
