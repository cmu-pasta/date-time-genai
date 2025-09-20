
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_last_weekday_in_month(year: int, month: int, weekday_int: int) -> pendulum.DateTime:
    """
    Finds the last occurrence of a specific weekday in a given month.

    Args:
        year (int): The year (e.g., 2023).
        month (int): The month (1-12).
        weekday_int (int): The integer representation of the weekday
                           (1 for Monday, 2 for Tuesday, ..., 7 for Sunday).

    Returns:
        pendulum.DateTime: A pendulum.DateTime object representing the last
                           occurrence of the specified weekday in the month,
                           with time set to midnight.
    """
    # Step 1: Create a pendulum.DateTime object for the first day of the specified month.
    # The exact day (1) doesn't matter for 'last_of' as it only uses year and month.
    start_of_month = pendulum.datetime(year, month, 1)

    # Step 2: Use the last_of method to find the last occurrence of the weekday in the month.
    # The 'weekday' parameter expects an integer from 1 (Monday) to 7 (Sunday).
    last_occurrence = start_of_month.last_of('month', weekday=weekday_int)
    
    # Step 3: Return the resulting pendulum.DateTime object.
    return last_occurrence

# Entry point: find_last_weekday_in_month(year: int, month: int, weekday_int: int) -> pendulum.DateTime

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
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_80_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_find_last_weekday_in_month(year, month, weekday_int):
    result = find_last_weekday_in_month(year, month, weekday_int)
    formatted_result = format_value_pd(result, year, month, weekday_int)
    log_file.write(formatted_result + "\n")
