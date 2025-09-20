
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def last_weekday_of_month(year: int, month: int, weekday: int) -> pendulum.Date:
    """
    Find the last occurrence of a specific weekday in a given month.

    Args:
        year (int): The target year (e.g., 2025).
        month (int): The target month (1-12).
        weekday (int): The target weekday where Monday=0 and Sunday=6.

    Returns:
        pendulum.Date: The date of the last occurrence of the specified weekday.
    """
    if month < 1 or month > 12:
        raise ValueError("month must be in 1..12")
    if weekday < 0 or weekday > 6:
        raise ValueError("weekday must be in 0..6 where Monday=0 and Sunday=6")

    # Get the last day of the month as a pendulum.Date
    last_day = pendulum.date(year, month, 1).end_of("month")

    # Calculate how many days to step back to reach the desired weekday
    # Example: if last_day is Friday (4) and weekday is Monday (0), delta = (4 - 0) % 7 = 4
    delta = (last_day.weekday() - weekday) % 7

    # Subtract the delta to land on the last desired weekday
    result = last_day.subtract(days=delta)

    return result

# Entry point: last_weekday_of_month(year: int, month: int, weekday: int) -> pendulum.Date

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_80_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_last_weekday_of_month(year, month, weekday):
    result = last_weekday_of_month(year, month, weekday)
    formatted_result = format_value_pd(result, year, month, weekday)
    log_file.write(formatted_result + "\n")
