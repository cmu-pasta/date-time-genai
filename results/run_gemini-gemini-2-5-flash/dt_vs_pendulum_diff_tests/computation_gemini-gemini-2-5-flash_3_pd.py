
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_next_leap_year(date: pendulum.DateTime) -> int:
    """
    Determines the next leap year after a given date.

    Args:
        date: The reference date (pendulum.DateTime).

    Returns:
        An integer representing the year of the next leap year.
    """
    current_year = date.year
    year_to_check = current_year + 1

    while True:
        # Create a pendulum.DateTime object for the first day of the year_to_check
        # This allows us to use the is_leap() method.
        test_date = pendulum.datetime(year_to_check, 1, 1)
        
        if test_date.is_leap():
            return year_to_check
        
        year_to_check += 1

# Entry point: find_next_leap_year(date: pendulum.DateTime) -> int

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_3_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_find_next_leap_year(date):
    result = find_next_leap_year(date)
    formatted_result = format_value_pd(result, date)
    log_file.write(formatted_result + "\n")
