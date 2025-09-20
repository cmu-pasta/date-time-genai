
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def date_to_julian_day_number(d: pendulum.Date) -> int:
    # Extract the Gregorian calendar components
    y = d.year
    m = d.month
    day = d.day

    # Algorithm: Proleptic Gregorian calendar to JDN
    a = (14 - m) // 12
    y2 = y + 4800 - a
    m2 = m + 12 * a - 3

    jdn = day + ((153 * m2 + 2) // 5) + 365 * y2 + (y2 // 4) - (y2 // 100) + (y2 // 400) - 32045
    return int(jdn)

# Entry point: date_to_julian_day_number(d: pendulum.Date) -> int

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_10_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_date_to_julian_day_number(d):
    result = date_to_julian_day_number(d)
    formatted_result = format_value_pd(result, d)
    log_file.write(formatted_result + "\n")
