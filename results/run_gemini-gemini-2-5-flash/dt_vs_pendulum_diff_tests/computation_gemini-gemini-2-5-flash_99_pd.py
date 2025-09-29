
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_decimal_time(time_of_day: pendulum.Time) -> float:
    # Step 1: Calculate the total number of seconds from midnight for the given time.
    # A pendulum.Time object has hour, minute, and second attributes.
    total_seconds_from_midnight = (
        time_of_day.hour * 3600 +
        time_of_day.minute * 60 +
        time_of_day.second
    )

    # Step 2: Determine the total number of seconds in a standard day.
    # 24 hours * 60 minutes/hour * 60 seconds/minute = 86400 seconds
    total_seconds_in_day = 86400.0 # Use float for division

    # Step 3: Calculate the decimal time representation.
    # This is the ratio of seconds elapsed from midnight to the total seconds in a day.
    decimal_time = total_seconds_from_midnight / total_seconds_in_day

    # Step 4: Return the result as a float.
    return decimal_time

# Entry point: calculate_decimal_time(time_of_day: pendulum.Time) -> float

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_99_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(time_strategy())
def test_calculate_decimal_time(time_of_day):
    result = calculate_decimal_time(time_of_day)
    formatted_result = format_value_pd(result, time_of_day)
    log_file.write(formatted_result + "\n")
