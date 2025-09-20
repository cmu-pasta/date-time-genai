
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_minutes_between_times(time1: pendulum.Time, time2: pendulum.Time) -> int:
    # Step 1: Create an arbitrary common date. Since the times are on the same day,
    # the specific date does not affect the minute difference.
    common_date = pendulum.date(2000, 1, 1)

    # Step 2: Combine the pendulum.Time objects with the common date to create
    # pendulum.DateTime objects.
    dt1 = common_date.at(time1.hour, time1.minute, time1.second, time1.microsecond)
    dt2 = common_date.at(time2.hour, time2.minute, time2.second, time2.microsecond)
    
    # Step 3: Calculate the difference between the two DateTime objects.
    # The result is a pendulum.Duration object.
    duration = dt1.diff(dt2)
    
    # Step 4: Extract the total number of minutes from the duration and return
    # its absolute value as an integer.
    return abs(duration.in_minutes())

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_33_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy(), time_strategy())
def test_calculate_minutes_between_times(time1, time2):
    result = calculate_minutes_between_times(time1, time2)
    formatted_result = format_value_pd(result, time1, time2)
    log_file.write(formatted_result + "\n")
