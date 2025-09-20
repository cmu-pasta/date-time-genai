
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def count_biweekly_periods_in_year(start_date: pendulum.Date, year: int) -> int:
    """
    Count the number of bi-weekly payroll periods (14-day cadence) that start within a given year.
    The cadence is anchored at the provided start_date (the start of a payroll period).
    """
    # Boundaries of the target year
    jan1 = pendulum.date(year, 1, 1)
    dec31 = pendulum.date(year, 12, 31)

    # Compute the minimal non-negative step n such that start_date + 14*n >= jan1
    # Let d = days from start_date to jan1 (can be negative)
    d = (jan1 - start_date).in_days()
    # Ceiling integer division for n = ceil(d / 14)
    n = -((-d) // 14)

    # First period start on or after Jan 1
    first_start = start_date.add(days=14 * n)

    # If the first period start is beyond the year end, no periods start in this year
    if first_start > dec31:
        return 0

    # Count how many 14-day starts fit within the year, inclusive
    remaining_days = (dec31 - first_start).in_days()
    count = 1 + (remaining_days // 14)
    return count

# Entry point: count_biweekly_periods_in_year(start_date: pendulum.Date, year: int) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_72_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy(), timestamp_strategy())
def test_count_biweekly_periods_in_year(start_date, year):
    result = count_biweekly_periods_in_year(start_date, year)
    formatted_result = format_value_pd(result, start_date, year)
    log_file.write(formatted_result + "\n")
