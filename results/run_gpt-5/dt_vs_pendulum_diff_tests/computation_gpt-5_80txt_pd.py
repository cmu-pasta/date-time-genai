
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def find_last_weekday_in_month(year: int, month: int, weekday: int) -> pendulum.Date:
    """
    Find the last occurrence of a specific weekday in a given month.

    Parameters:
    - year: Integer year (e.g., 2025)
    - month: Integer month 1-12
    - weekday: Integer weekday where Monday=0 ... Sunday=6

    Returns:
    - pendulum.Date representing the last occurrence of the specified weekday in the given month.
    """
    if not (1 <= month <= 12):
        raise ValueError("month must be in 1..12")
    if not (0 <= weekday <= 6):
        raise ValueError("weekday must be in 0..6 (Monday=0 ... Sunday=6)")

    # First day of the given month
    first_day = pendulum.date(year, month, 1)

    # Last day of the month: go to first day of next month, then subtract one day
    last_day = first_day.add(months=1).subtract(days=1)

    # Compute offset back to the target weekday
    offset = (last_day.weekday() - weekday) % 7

    # The last occurrence of the target weekday
    result = last_day.subtract(days=offset)

    return result

# Entry point: find_last_weekday_in_month(year: int, month: int, weekday: int) -> pendulum.Date

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_80txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_find_last_weekday_in_month(year, month, weekday):
    result = find_last_weekday_in_month(year, month, weekday)
    formatted_result = format_value_pd(result, year, month, weekday)
    log_file.write(formatted_result + "\n")
