
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def date_year_to_roman(d: date) -> str:
    # Step 1: Extract the year from the date
    y = d.year

    # Step 2: Validate the year (standard Roman numerals cover 1..3999)
    if y < 1 or y > 3999:
        raise ValueError("Year out of range for standard Roman numerals (1..3999).")

    # Step 3: Convert to Roman numeral using positional mapping
    thousands = ["", "M", "MM", "MMM"]
    hundreds  = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
    tens      = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
    ones      = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]

    roman = (
        thousands[y // 1000] +
        hundreds[(y % 1000) // 100] +
        tens[(y % 100) // 10] +
        ones[y % 10]
    )

    # Step 4: Return the Roman numeral representation
    return roman

# Entry point: date_year_to_roman(d: date) -> str

def format_value_dt(*values):
    formatted_values = []

    for value in values:
        if isinstance(value, datetime):
            formatted_values.append(value.isoformat())
        elif isinstance(value, date):
            # Use strftime to format the date similar to to_date_string()
            formatted_values.append(value.strftime("%Y-%m-%d"))
        elif isinstance(value, time):
            formatted_values.append(value.isoformat())
        elif isinstance(value, timedelta):
            formatted_values.append(str(value.total_seconds()))
        else:
            formatted_values.append(str(value))

    return ", ".join(formatted_values)

if not os.path.exists("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs"):
    os.makedirs("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_52_a.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_date_year_to_roman(d):
    result = date_year_to_roman(d)
    formatted_result = format_value_dt(result, d)
    log_file.write(formatted_result + "\n")
