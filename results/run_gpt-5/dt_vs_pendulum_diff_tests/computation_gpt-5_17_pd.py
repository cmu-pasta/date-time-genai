
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def nth_weekday_in_month(year: int, month: int, weekday: int, n: int) -> pendulum.Date:
    # Validate inputs
    if not (1 <= month <= 12):
        raise ValueError("month must be between 1 and 12.")
    if not (0 <= weekday <= 6):
        raise ValueError("weekday must be between 0 (Monday) and 6 (Sunday).")
    if n < 1:
        raise ValueError("n must be a positive integer (1 for first occurrence, etc.).")

    # First day of the month
    first_day = pendulum.date(year, month, 1)

    # Offset to the first desired weekday in the month
    offset_days = (weekday - first_day.weekday()) % 7
    first_occurrence = first_day.add(days=offset_days)

    # Compute the nth occurrence
    nth_date = first_occurrence.add(weeks=n - 1)

    # Ensure the nth occurrence is within the same month
    if nth_date.month != month:
        raise ValueError("The specified nth occurrence does not exist in this month.")

    return nth_date

# Entry point: nth_weekday_in_month(year: int, month: int, weekday: int, n: int) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_17_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_nth_weekday_in_month(year, month, weekday, n):
    result = nth_weekday_in_month(year, month, weekday, n)
    formatted_result = format_value_pd(result, year, month, weekday, n)
    log_file.write(formatted_result + "\n")
