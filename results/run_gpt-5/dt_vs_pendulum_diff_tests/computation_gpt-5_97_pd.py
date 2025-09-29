
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def thai_buddhist_date_yyyymmdd(gregorian_date: pendulum.Date) -> int:
    """
    Convert a Gregorian date to the Thai Buddhist calendar date and return it as an integer YYYYMMDD.
    - Input: pendulum.Date (Gregorian)
    - Output: int representing BE date as YYYYMMDD
    """
    be_year = gregorian_date.year + 543
    month = gregorian_date.month
    day = gregorian_date.day

    # Encode as YYYYMMDD integer to satisfy allowed output types without constructing a non-Gregorian date
    return be_year * 10000 + month * 100 + day

# Entry point: thai_buddhist_date_yyyymmdd(gregorian_date: pendulum.Date) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_97_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_thai_buddhist_date_yyyymmdd(gregorian_date):
    result = thai_buddhist_date_yyyymmdd(gregorian_date)
    formatted_result = format_value_pd(result, gregorian_date)
    log_file.write(formatted_result + "\n")
