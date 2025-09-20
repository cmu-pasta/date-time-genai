
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def convert_year_to_roman_numeral(dt: pendulum.DateTime) -> str:
    """
    Converts the year of a given pendulum.DateTime object into its Roman numeral representation.

    Args:
        dt (pendulum.DateTime): The date from which to extract the year.

    Returns:
        str: The Roman numeral representation of the year.
    """
    year = dt.year
    roman_map = {
        1000: 'M', 900: 'CM', 500: 'D', 400: 'CD', 100: 'C',
        90: 'XC', 50: 'L', 40: 'XL', 10: 'X', 9: 'IX', 5: 'V',
        4: 'IV', 1: 'I'
    }
    
    roman_numeral = []
    for value, symbol in roman_map.items():
        while year >= value:
            roman_numeral.append(symbol)
            year -= value
    
    return "".join(roman_numeral)

# Entry point: convert_year_to_roman_numeral(dt: pendulum.DateTime) -> str

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

if not os.path.exists("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_gemini-gemini-2-5-flash/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_gemini-gemini-2-5-flash_52_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(datetime_strategy())
def test_convert_year_to_roman_numeral(dt):
    result = convert_year_to_roman_numeral(dt)
    formatted_result = format_value_pd(result, dt)
    log_file.write(formatted_result + "\n")
