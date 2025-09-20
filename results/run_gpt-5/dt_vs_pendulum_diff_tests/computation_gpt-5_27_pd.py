
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def count_leap_years_between(year1: int, year2: int) -> int:
    """
    Count the number of leap years between two years inclusively.
    Uses pendulum's is_leap_year property on a DateTime instance for each year.
    """
    # Step 1: Normalize the range
    start = year1 if year1 <= year2 else year2
    end = year2 if year2 >= year1 else year1

    # Step 2: Iterate over the years and count leap years using Pendulum
    count = 0
    year = start
    while year <= end:
        if pendulum.datetime(year, 1, 1).is_leap_year:
            count += 1
        year += 1

    # Step 3: Return the count as an integer
    return count

# Entry point: count_leap_years_between(year1: int, year2: int) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_27_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy())
def test_count_leap_years_between(year1, year2):
    result = count_leap_years_between(year1, year2)
    formatted_result = format_value_pd(result, year1, year2)
    log_file.write(formatted_result + "\n")
