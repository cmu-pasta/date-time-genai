
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def memorial_day(year: int) -> pendulum.Date:
    """
    Compute the date of Memorial Day for a given year (last Monday of May).
    
    Args:
        year (int): The target year.
        
    Returns:
        pendulum.Date: The date of Memorial Day in the given year.
    """
    may_31 = pendulum.date(year, 5, 31)
    weekday = may_31.weekday()  # Monday=0 ... Sunday=6
    offset = (weekday - pendulum.MONDAY) % 7  # days to step back to Monday
    return may_31.subtract(days=offset)

# Entry point: memorial_day(year: int) -> pendulum.Date

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_47txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_memorial_day(year):
    result = memorial_day(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
