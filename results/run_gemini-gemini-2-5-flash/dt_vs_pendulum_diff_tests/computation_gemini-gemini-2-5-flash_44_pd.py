
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def get_first_day_of_spring(year: int) -> pendulum.Date:
    """
    Finds the date of the first day of spring for a given year.
    For the purpose of this computation, the first day of spring is approximated
    as March 20th of the given year, which is a common convention for the
    vernal equinox in the Northern Hemisphere.

    Args:
        year: An integer representing the year.

    Returns:
        A pendulum.Date object representing March 20th of the given year.
    """
    # Step 1: Construct a pendulum.Date object for March 20th of the given year.
    # We use 3 for March and 20 for the day.
    first_day_of_spring = pendulum.date(year, 3, 20)
    
    # Step 2: Return the resulting date.
    return first_day_of_spring

# Entry point: get_first_day_of_spring(year: int) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_44_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_get_first_day_of_spring(year):
    result = get_first_day_of_spring(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
