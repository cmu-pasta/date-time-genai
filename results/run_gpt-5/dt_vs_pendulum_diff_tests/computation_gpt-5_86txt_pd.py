
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def presidents_day(year: int) -> pendulum.Date:
    """
    Compute Presidents' Day (third Monday of February) for the given year.

    Args:
        year (int): The target year.

    Returns:
        pendulum.Date: The date of Presidents' Day for the given year.
    """
    # Step 1: February 1st of the given year
    feb_first = pendulum.date(year, 2, 1)
    # Step 2: Day of week for Feb 1st (Monday=0, ..., Sunday=6)
    dow = feb_first.day_of_week
    # Step 3: Offset to first Monday on or after Feb 1st
    offset_to_monday = (0 - dow) % 7  # 0 represents Monday
    first_monday = feb_first.add(days=offset_to_monday)
    # Step 4: Third Monday = first Monday + 14 days
    third_monday = first_monday.add(days=14)
    # Step 5: Return the pendulum.Date
    return third_monday

# Entry point: presidents_day(year: int) -> pendulum.Date

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_86txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_presidents_day(year):
    result = presidents_day(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
