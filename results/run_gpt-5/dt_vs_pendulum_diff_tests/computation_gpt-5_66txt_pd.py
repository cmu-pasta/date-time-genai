
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def trading_days_in_year(year: int) -> int:
    """
    Calculate the number of trading days (Monday-Friday) in the specified year.
    """
    # Step 1: Initialize the start date for the given year
    current = pendulum.date(year, 1, 1)
    count = 0

    # Step 2: Iterate through the year, counting weekdays (Mon-Fri)
    while current.year == year:
        if current.day_of_week < 5:  # Monday=0, ..., Friday=4
            count += 1
        current = current.add(days=1)

    # Step 3: Return the total number of trading days
    return count

# Entry point: trading_days_in_year(year: int) -> int

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_66txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_trading_days_in_year(year):
    result = trading_days_in_year(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
