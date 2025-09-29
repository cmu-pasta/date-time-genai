
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_chronological_age_in_seconds(birth_datetime: pendulum.DateTime) -> int:
    # Step 1: Get the current datetime. It's good practice to ensure consistent timezones for accurate calculation.
    # If birth_datetime is naive, pendulum.now() (which is aware) will handle the comparison.
    # For robust solutions, one might normalize timezones (e.g., to UTC).
    current_datetime = pendulum.now(birth_datetime.timezone if birth_datetime.tzinfo else None)

    # Step 2: Calculate the duration between the current datetime and the birth datetime.
    # This results in a pendulum.Duration object.
    duration = current_datetime - birth_datetime

    # Step 3: Get the total number of seconds from the duration.
    # total_seconds() returns a float.
    total_seconds_float = duration.total_seconds()

    # Step 4: Convert the result to an integer and take the absolute value
    # to ensure a positive age in seconds.
    age_in_seconds = int(abs(total_seconds_float))
    
    return age_in_seconds

# Entry point: calculate_chronological_age_in_seconds(birth_datetime: pendulum.DateTime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_75_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_chronological_age_in_seconds(birth_datetime):
    result = calculate_chronological_age_in_seconds(birth_datetime)
    formatted_result = format_value_pd(result, birth_datetime)
    log_file.write(formatted_result + "\n")
