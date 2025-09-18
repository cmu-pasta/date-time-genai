
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def is_leap_year(year: int) -> bool:
    # Step 1: Create a pendulum.DateTime object for the given year.
    # The day and month (e.g., January 1st) don't affect the leap year check for the year itself.
    date_in_year = pendulum.datetime(year, 1, 1)
    
    # Step 2: Use the is_leap() method available on pendulum.DateTime objects.
    # This method returns True if the year of the object is a leap year, False otherwise.
    is_leap = date_in_year.is_leap()
    
    # Step 3: Return the boolean result.
    return is_leap

# Entry point: is_leap_year(year: int) -> bool

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_7_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_is_leap_year(year):
    result = is_leap_year(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
