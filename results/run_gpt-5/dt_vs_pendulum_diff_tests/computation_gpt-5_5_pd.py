
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def first_monday_of_month(year: int, month: int) -> pendulum.Date:
    """
    Compute the first Monday for the specified month and year.
    Inputs:
      - year: integer year (e.g., 2025)
      - month: integer month in 1..12
    Output:
      - pendulum.Date corresponding to the first Monday of that month
    """
    first_day = pendulum.date(year, month, 1)
    # Monday is 0, Sunday is 6
    weekday_index = first_day.weekday()
    # Days to add to reach the first Monday (0..6)
    offset_days = (0 - weekday_index) % 7
    return first_day.add(days=offset_days)

# Entry point: first_monday_of_month(year: int, month: int) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_5_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy())
def test_first_monday_of_month(year, month):
    result = first_monday_of_month(year, month)
    formatted_result = format_value_pd(result, year, month)
    log_file.write(formatted_result + "\n")
