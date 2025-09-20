
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date
def _int_to_roman(n: int) -> str:
    if n <= 0:
        raise ValueError("Year must be a positive integer.")
    # Standard Roman numeral mapping for subtractive notation
    vals = (1000, 900, 500, 400, 100, 90,  50,  40,  10,  9,   5,   4,   1)
    syms = ("M",  "CM","D", "CD","C","XC","L","XL","X","IX","V","IV","I")
    result = []
    for v, s in zip(vals, syms):
        if n == 0:
            break
        count, n = divmod(n, v)
        if count:
            result.append(s * count)
    return "".join(result)

def date_to_roman_year(d: date) -> str:
    # Extract the year from the given date and convert to Roman numerals
    return _int_to_roman(d.year)

# Entry point: date_to_roman_year(d: date) -> str

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
log_file = open(os.path.join("./results/run_gpt-5/.logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_52_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_date_to_roman_year(d):
    result = date_to_roman_year(d)
    formatted_result = format_value_dt(result, d)
    log_file.write(formatted_result + "\n")
