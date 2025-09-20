
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def _julian_to_jdn(year: int, month: int, day: int) -> int:
    # Convert a Julian calendar date to Julian Day Number (JDN)
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    jdn = day + ((153 * m + 2) // 5) + 365 * y + (y // 4) - 32083
    return jdn

def _jdn_to_gregorian_date(jdn: int) -> pendulum.Date:
    # Convert Julian Day Number (JDN) to a Gregorian calendar date
    a = jdn + 32044
    b = (4 * a + 3) // 146097
    c = a - (146097 * b) // 4
    d = (4 * c + 3) // 1461
    e = c - (1461 * d) // 4
    m = (5 * e + 2) // 153
    day = e - (153 * m + 2) // 5 + 1
    month = m + 3 - 12 * (m // 10)
    year = 100 * b + d - 4800 + (m // 10)
    return pendulum.date(year, month, day)

def convert_julian_to_gregorian(year: int, month: int, day: int) -> pendulum.Date:
    # Step 1: Convert the Julian calendar date to JDN
    jdn = _julian_to_jdn(year, month, day)
    # Step 2: Convert JDN to Gregorian date and return as pendulum.Date
    return _jdn_to_gregorian_date(jdn)

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

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_70_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(timestamp_strategy(), timestamp_strategy(), timestamp_strategy())
def test_convert_julian_to_gregorian(year, month, day):
    result = convert_julian_to_gregorian(year, month, day)
    formatted_result = format_value_pd(result, year, month, day)
    log_file.write(formatted_result + "\n")
