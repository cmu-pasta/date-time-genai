
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def mlk_day(year: int) -> pendulum.Date:
    """
    Compute Martin Luther King Jr. Day (third Monday of January) for a given year.

    :param year: The target year as an integer.
    :return: A pendulum.Date representing the third Monday of January of the given year.
    """
    jan_first = pendulum.date(year, 1, 1)
    # day_of_week: Monday=0, Sunday=6 in pendulum
    days_to_first_monday = (pendulum.MONDAY - jan_first.day_of_week) % 7
    first_monday = jan_first.add(days=days_to_first_monday)
    third_monday = first_monday.add(weeks=2)
    return third_monday

# Entry point: mlk_day(year: int) -> pendulum.Date

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_92_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_mlk_day(year):
    result = mlk_day(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
