
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def _int_to_roman(year: int) -> str:
    # Supports 1..3999 (standard Roman numerals)
    if year <= 0 or year > 3999:
        # Roman numerals traditionally represent 1..3999
        # You may adjust this behavior as needed.
        raise ValueError("Year out of representable range for Roman numerals (1..3999)")

    mapping = (
        (1000, "M"),
        (900,  "CM"),
        (500,  "D"),
        (400,  "CD"),
        (100,  "C"),
        (90,   "XC"),
        (50,   "L"),
        (40,   "XL"),
        (10,   "X"),
        (9,    "IX"),
        (5,    "V"),
        (4,    "IV"),
        (1,    "I"),
    )

    result = []
    n = year
    for value, symbol in mapping:
        if n == 0:
            break
        count, n = divmod(n, value)
        if count:
            result.append(symbol * count)
    return "".join(result)

def date_year_to_roman(dt: pendulum.Date) -> str:
    # Accepts pendulum.Date or pendulum.DateTime thanks to duck-typing of .year
    # Extract the year and convert it to a Roman numeral string
    year = dt.year
    return _int_to_roman(year)

# Entry point: date_year_to_roman(dt: pendulum.Date) -> str

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gpt-5_52_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_date_year_to_roman(dt):
    result = date_year_to_roman(dt)
    formatted_result = format_value_pd(result, dt)
    log_file.write(formatted_result + "\n")
