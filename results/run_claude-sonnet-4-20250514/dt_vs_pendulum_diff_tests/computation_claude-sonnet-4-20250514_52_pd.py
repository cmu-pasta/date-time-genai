
import pendulum
import os

from pendulum_generators import *
from hypothesis import settings, seed, given

import pendulum
def date_to_roman_year(date: pendulum.Date) -> str:
    # Step 1: Extract the year from the date
    year = date.year
    
    # Step 2: Convert year to Roman numerals
    def int_to_roman(num):
        # Define the mapping of values to Roman numerals
        values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        symbols = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
        
        roman_num = ""
        for i in range(len(values)):
            count = num // values[i]
            if count:
                roman_num += symbols[i] * count
                num -= values[i] * count
        return roman_num
    
    # Step 3: Convert the year to Roman numerals
    roman_year = int_to_roman(year)
    
    # Step 4: Return the result
    return roman_year

# Entry point: date_to_roman_year(date: pendulum.Date) -> str

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

if not os.path.exists("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs"):
    os.makedirs("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs")
log_file = open(os.path.join("./results/run_claude-sonnet-4-20250514/.logs/dt_vs_pendulum_diff_test_logs", "log_computation_claude-sonnet-4-20250514_52_pendulum.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_date_to_roman_year(date):
    result = date_to_roman_year(date)
    formatted_result = format_value_pd(result, date)
    log_file.write(formatted_result + "\n")
