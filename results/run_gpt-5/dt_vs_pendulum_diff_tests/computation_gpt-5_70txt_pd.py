
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def convert_julian_to_gregorian(year: int, month: int, day: int) -> pendulum.Date:
    """
    Convert a Julian calendar date (year, month, day) to the corresponding Gregorian calendar date.
    Inputs are integers; output is a pendulum.Date.

    Assumptions:
    - The input date is valid in the Julian calendar.
    - The conversion uses standard astronomical algorithms (proleptic where applicable).
    """

    # Step 1: Convert Julian calendar date to Julian Day Number (JDN)
    # Algorithm for Julian calendar to JDN
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    jdn = day + ((153 * m + 2) // 5) + 365 * y + (y // 4) - 32083

    # Step 2: Convert JDN to Gregorian calendar date (Fliegel–Van Flandern algorithm)
    l = jdn + 68569
    n = (4 * l) // 146097
    l = l - (146097 * n + 3) // 4
    i = (4000 * (l + 1)) // 1461001
    l = l - (1461 * i) // 4 + 31
    j = (80 * l) // 2447
    d = l - (2447 * j) // 80
    l = j // 11
    m = j + 2 - 12 * l
    y = 100 * (n - 49) + i + l

    # Step 3: Build and return a pendulum.Date in the Gregorian calendar
    return pendulum.date(y, m, d)

# Entry point: convert_julian_to_gregorian(year: int, month: int, day: int) -> pendulum.Date

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
log_file = open(os.path.join(".logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_70txt_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_convert_julian_to_gregorian(year, month, day):
    result = convert_julian_to_gregorian(year, month, day)
    formatted_result = format_value_pd(result, year, month, day)
    log_file.write(formatted_result + "\n")
