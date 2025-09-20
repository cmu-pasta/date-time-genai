
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def get_day_number_of_week(dt: pendulum.DateTime) -> int:
    # Step 1: Access the day_of_week property of the pendulum.DateTime object.
    # Pendulum's day_of_week returns 1 for Monday and 7 for Sunday (ISO 8601).
    day_number = dt.day_of_week
    
    # Step 2: Return the integer representation of the day number.
    return day_number

# Entry point: get_day_number_of_week(dt: pendulum.DateTime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_61_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_get_day_number_of_week(dt):
    result = get_day_number_of_week(dt)
    formatted_result = format_value_pd(result, dt)
    log_file.write(formatted_result + "\n")
