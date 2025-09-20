
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def memorial_day(year: int) -> pendulum.Date:
    """
    Compute Memorial Day (last Monday of May) for the given year.
    Returns a pendulum.Date.
    """
    may_31 = pendulum.date(year, 5, 31)
    # weekday(): 0=Monday, ..., 6=Sunday
    offset = may_31.weekday()
    last_monday = may_31.subtract(days=offset)
    return last_monday

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_47_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy())
def test_memorial_day(year):
    result = memorial_day(year)
    formatted_result = format_value_pd(result, year)
    log_file.write(formatted_result + "\n")
