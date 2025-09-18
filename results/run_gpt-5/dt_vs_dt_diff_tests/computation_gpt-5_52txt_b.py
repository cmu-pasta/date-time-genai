
import os

from datetime import date, datetime, time, timedelta, timezone
from datetime_generators import *
from hypothesis import given, seed, settings

from datetime import date, datetime
def _int_to_roman(year: int) -> str:
    """
    Convert an integer year (1..3999) to its Roman numeral representation.
    """
    if year < 1 or year > 3999:
        raise ValueError("Year out of supported range (1..3999) for Roman numeral conversion.")
    
    val = (1000, 900, 500, 400, 100, 90,  50,  40,  10,  9,   5,   4,   1)
    syms = ("M",  "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I")
    
    result = []
    n = year
    for v, s in zip(val, syms):
        count, n = divmod(n, v)
        if count:
            result.append(s * count)
        if n == 0:
            break
    return "".join(result)

def date_to_roman_year(d: date) -> str:
    """
    Convert the year of a given date/datetime to its Roman numeral representation.
    Accepts:
      - datetime.date
      - datetime.datetime (subclass of date)
    Returns:
      - str Roman numeral of the year (supports 1..3999)
    """
    year = d.year  # datetime.datetime is a subclass of date; both have .year
    return _int_to_roman(year)

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

if not os.path.exists(".logs/dt_vs_dt_diff_test_logs"):
    os.makedirs(".logs/dt_vs_dt_diff_test_logs")
log_file = open(os.path.join(".logs/dt_vs_dt_diff_test_logs", "log_computation_gpt-5_52txt_b.txt"), "w")

@seed(27)
@settings(max_examples=10000, deadline=None, derandomize=True)
@given(date_strategy())
def test_date_to_roman_year(d):
    result = date_to_roman_year(d)
    formatted_result = format_value_dt(result, d)
    log_file.write(formatted_result + "\n")
