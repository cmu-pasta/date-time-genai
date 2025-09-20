
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def calculate_percentage_of_year_passed(dt: pendulum.DateTime) -> float:
    # Step 1: Get the total number of days in the year for the given date.
    total_days_in_year = dt.days_in_year

    # Step 2: Get the number of days that have passed up to (but not including) the current date.
    # day_of_year is 1-indexed, so subtract 1 to get days passed.
    days_passed = dt.day_of_year - 1
    
    # Step 3: Calculate the percentage.
    # Ensure float division by casting one of the operands to float.
    percentage = (float(days_passed) / total_days_in_year) * 100
    
    # Step 4: Return the result as a float.
    return percentage

# Entry point: calculate_percentage_of_year_passed(dt: pendulum.DateTime) -> float

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_54_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_calculate_percentage_of_year_passed(dt):
    result = calculate_percentage_of_year_passed(dt)
    formatted_result = format_value_pd(result, dt)
    log_file.write(formatted_result + "\n")
