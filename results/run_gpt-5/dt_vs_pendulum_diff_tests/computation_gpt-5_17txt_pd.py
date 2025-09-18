
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_nth_weekday_in_month(year: int, month: int, target_weekday: int, n: int) -> pendulum.Date:
    """
    Find the nth occurrence of a specific weekday in a given month and year.

    Parameters:
    - year: Calendar year (e.g., 2025)
    - month: Month number (1-12)
    - target_weekday: Weekday as integer where Monday=0 and Sunday=6
    - n: The occurrence index (1 for first, 2 for second, ...)

    Returns:
    - pendulum.Date representing the date of the nth occurrence.

    Raises:
    - ValueError if inputs are invalid or the nth occurrence does not exist in the month.
    """
    # Basic input validation
    if not (1 <= month <= 12):
        raise ValueError("month must be in 1..12")
    if not (0 <= target_weekday <= 6):
        raise ValueError("target_weekday must be in 0..6 (Monday=0 ... Sunday=6)")
    if n < 1:
        raise ValueError("n must be >= 1")

    # First day of the month
    first_of_month: pendulum.Date = pendulum.date(year, month, 1)

    # Days to the first target weekday in the month
    days_until_first = (target_weekday - first_of_month.weekday()) % 7

    # First occurrence of the target weekday
    first_occurrence: pendulum.Date = first_of_month.add(days=days_until_first)

    # Compute the nth occurrence by adding (n-1) weeks
    nth_occurrence: pendulum.Date = first_occurrence.add(weeks=n - 1)

    # Ensure the nth occurrence is still within the same month
    if nth_occurrence.month != month:
        raise ValueError("The requested nth occurrence does not exist in the given month.")

    return nth_occurrence

# Entry point: find_nth_weekday_in_month(year: int, month: int, target_weekday: int, n: int) -> pendulum.Date

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_17txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_find_nth_weekday_in_month(year, month, target_weekday, n):
    result = find_nth_weekday_in_month(year, month, target_weekday, n)
    formatted_result = format_value_pd(result, year, month, target_weekday, n)
    log_file.write(formatted_result + "\n")
