
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def labor_day(year: int) -> pendulum.Date:
    """
    Compute Labor Day (first Monday of September) for a given year.

    Args:
        year (int): The year for which to compute Labor Day.

    Returns:
        pendulum.Date: The date of Labor Day in the given year.
    """
    sept_first = pendulum.date(year, 9, 1)
    # Monday is 0 in pendulum's day_of_week
    days_to_add = (0 - sept_first.day_of_week) % 7
    labor_day_date = sept_first.add(days=days_to_add)
    return labor_day_date

# Entry point: labor_day(year: int) -> pendulum.Date

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_68txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_labor_day(year):
    result = labor_day(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
